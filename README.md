# 🌀 Scraper Quântico

Motor de extração de conteúdo web ultra-leve para o ecossistema **Atena**.

**Tamanho:** ~80 MB 🪶 (95% menor que Crawl4AI)

## Como usar

```bash
# Extrair uma página
curl -X POST https://scraper-quantico.onrender.com/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://exemplo.com"}'

# Extrair várias
curl -X POST https://scraper-quantico.onrender.com/batch \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://site1.com", "https://site2.com"]}'

# Health check
curl https://scraper-quantico.onrender.com/health
```

## Integração com n8n

Use o nó **HTTP Request** apontando para o Scraper Quântico.