"""
🌀 Scraper Quântico — Atena Ecosystem
Motor de extração de conteúdo web ultra-leve.
Sem browser, sem Chromium, sem peso morto.
"""

import trafilatura
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(
    title="🌀 Scraper Quântico",
    description="Extrator de conteúdo web leve para o ecossistema Atena",
    version="0.1.0",
)


class ScrapeRequest(BaseModel):
    url: str
    output_format: Optional[str] = "markdown"
    include_links: Optional[bool] = True
    include_images: Optional[bool] = False


class ScrapeResponse(BaseModel):
    url: str
    title: Optional[str] = None
    content: Optional[str] = None
    format: str
    success: bool
    error: Optional[str] = None


@app.get("/health")
def health():
    return {"status": "ok", "service": "scraper-quantico", "version": "0.1.0"}


@app.post("/scrape", response_model=ScrapeResponse)
def scrape(req: ScrapeRequest):
    try:
        downloaded = trafilatura.fetch_url(req.url)
        if not downloaded:
            raise HTTPException(
                status_code=400, detail=f"Nao foi possivel acessar {req.url}"
            )

        result = trafilatura.extract(
            downloaded,
            output_format=req.output_format,
            include_links=req.include_links,
            include_images=req.include_images,
            with_metadata=True,
        )

        if not result:
            raise HTTPException(
                status_code=400, detail="Nao foi possivel extrair conteudo"
            )

        metadata = trafilatura.extract_metadata(downloaded)

        content = result if isinstance(result, str) else result.get("text", "")

        return ScrapeResponse(
            url=req.url,
            title=metadata.title if metadata else None,
            content=content,
            format=req.output_format,
            success=True,
        )
    except HTTPException:
        raise
    except Exception as e:
        return ScrapeResponse(
            url=req.url,
            success=False,
            error=str(e),
            format=req.output_format,
        )


@app.post("/batch")
def batch_scrape(urls: List[str]):
    results = []
    for url in urls:
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                content = trafilatura.extract(downloaded, output_format="markdown")
                metadata = trafilatura.extract_metadata(downloaded)
                results.append(
                    {
                        "url": url,
                        "title": metadata.title if metadata else None,
                        "content": content,
                        "success": True,
                    }
                )
            else:
                results.append({"url": url, "success": False, "error": "Inaccessible"})
        except Exception as e:
            results.append({"url": url, "success": False, "error": str(e)})

    return {"results": results}