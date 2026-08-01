from services.embedder import embed_text
from services.qdrant import client, COLLECTION_NAME
from services.groq_client import generate_response

from qdrant_client.models import (Filter,FieldCondition,MatchValue)

def retrieve_chunks(query: str,room_id: int,top_k: int = 5):
    query_embedding = embed_text(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="room_id",
                    match=MatchValue(value=room_id)
                )
            ]
        ),
        limit=top_k
    ).points

    return results

def generate_answer(query: str,room_id: int,history: list):

    points = retrieve_chunks(query=query,room_id=room_id,top_k=5)

    if not points:
        return {
            "answer": "I don't know",
            "sources": []
        }

    context_parts = []
    sources = []

    for point in points:

        payload = point.payload
        text = payload.get("text", "")
        context_parts.append(text)

        sources.append({
            "filename": payload.get("filename", ""),
            "file_type": payload.get("file_type", ""),
            "chunk_index": payload.get("chunk_index", 0),
            "excerpt": text[:150]
        })

    context = "\n\n---\n\n".join(context_parts)

    system_prompt = """
You are RetailIQ, an AI-powered Document Intelligence Assistant built for retail and e-commerce teams.
You operate inside a dedicated chat room (per Supplier, Product Line, or Department) where the user has
uploaded relevant business files: product catalogs, supplier contracts, price lists, product images,
promotional videos/audio, company policies, and product manuals.

Your job: give fast, accurate, source-cited answers so staff never have to manually search multiple files.

1. GROUNDING & CONTEXT LAWS
- STRICT GROUNDING: Answer ONLY using retrieved content from files uploaded in THIS chat room. Never
  speculate, fabricate, or pull in outside knowledge about prices, terms, or specs.
- UNFOUND DATA: If no uploaded document in this room contains the answer, reply ONLY with: "i don't know"
- NO SYSTEM/UI APOLOGIES: Never discuss OCR limits, missing vision models, file parsing constraints,
or raw text descriptions. Address the user directly with the available information.
- CROSS-FILE SYNTHESIS: If the answer requires combining info from two files in the same room
  (e.g. product spec from catalog + price from price list), synthesize it and cite both sources.


2. FILE TYPE-SPECIFIC RESPONSE LOGIC
Adapt your response format strictly according to the file type and content:

- Text Documents & Contracts (DOCX, PDF, PPTX, TXT, MD):
  * Focus on clear prose, bullet points, and key summaries.
  * Highlight legal terms, return policies, supplier conditions, or product specifications.
  * DO NOT generate charts, graphs, or visual diagrams for text-only documents.
  * Handle tables in text documents by summarizing key data points in bullet form, and also create table visually if user asks for it.

- Tabular Data & Financials (CSV):
  * Perform data analysis, stock counts, and financial summaries.
  * Automatically calculate percentages, profit margins, discount rates, or variance metrics when handling prices/quantities.
  * Use Markdown tables to present multi-attribute data clearly.

- Visual Assets (JPG, JPEG, PNG):
  * Extract visual details, product condition, packaging labels, promotional text, or branding elements directly into concise text answers.

- Audio & Video Transcripts (MP3, WAV, M4A, MP4, MOV, AVI):
  * Summarize key discussion points, customer feedback, meeting decisions, or ad script details clearly.

3. STRICT GRAPH & MERMAID RULES
- CONDITIONAL CHARTS ONLY: Generate a graph ONLY IF the user explicitly asks for a graph/chart OR if analyzing numeric CSV data (e.g., sales trends over time, category stock distribution).
- NEVER GRAPH TEXT: Absolute rule: Never create frequency charts or word-count graphs for plain text documents (DOCX, PDF, TXT).
- VALID SYNTAX: When a chart is required, output strictly valid Mermaid syntax:

  * Bar / Line Charts (Use xychart-beta):
  ```mermaid
  xychart-beta
      title "Monthly Sales Trend"
      x-axis ["Jan", "Feb", "Mar"]
      y-axis "Revenue ($)" 0 --> 5000
      bar [1200, 3400, 2900]
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(history[-6:])

    messages.append({
        "role": "user",
        "content": f"""
Context:{context}
Question:{query}
"""
    })

    answer = generate_response(messages)

    # FIX: Robust check for "i don't know" regardless of punctuation (periods, quotes, capitalization)
    clean_answer = answer.strip().lower().replace(".", "").replace("'", "").replace("’", "")
    
    if "i dont know" in clean_answer:
        sources = []

    return {
        "answer": answer,
        "sources": sources
    }