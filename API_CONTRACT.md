# API Contract — CSN Chatbot

## Gemensamt endpoint-format
Alla tre backends exponerar samma endpoint-struktur.

## Endpoint
POST /chat

## Request
```json
{
  "question": "Hur mycket kan jag låna?"
}
```

## Response
```json
{
  "answer": "Du kan låna upp till...",
  "sources": ["https://www.csn.se/bidrag-och-lan/..."]
}
```

## Portar
- Orhan (Studiestöd): port 8001
- Henke (Återbetalning): port 8002
- Mona (Utlandsstudier): port 8003

## Felhantering
```json
{
  "detail": "Något gick fel"
}
```