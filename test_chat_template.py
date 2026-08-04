
import json

from jinja2 import Environment, FileSystemLoader, StrictUndefined


def raise_exception(message):
    raise ValueError(message)


environment = Environment(
    loader=FileSystemLoader("."),
    undefined=StrictUndefined,
    trim_blocks=True,
    lstrip_blocks=True,
)

environment.globals["raise_exception"] = raise_exception

template = environment.get_template("chat_template.jinja")


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_books",
            "description": "Kitapları başlık veya yazar adına göre arar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Aranacak kitap veya yazar adı",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_order",
            "description": "Stoktaki bir kitap için sipariş oluşturur.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Sipariş edilecek kitabın adı",
                    },
                    "quantity": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "Sipariş miktarı",
                    },
                },
                "required": ["title", "quantity"],
            },
        },
    },
]


messages = [
    {
        "role": "system",
        "content": (
            "Sen bir kitapçı asistanısın. "
            "Sadece araçlardan dönen gerçek verilere dayan."
        ),
    },
    {
        "role": "user",
        "content": "Kürk Mantolu Madonna stokta var mı?",
    },
    {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {
                "type": "function",
                "function": {
                    "name": "search_books",
                    "arguments": {
                        "query": "Kürk Mantolu Madonna"
                    },
                },
            }
        ],
    },
    {
        "role": "tool",
        "name": "search_books",
        "content": json.dumps(
            {
                "found": True,
                "title": "Kürk Mantolu Madonna",
                "author": "Sabahattin Ali",
                "price": 120,
                "stock": 8,
            },
            ensure_ascii=False,
        ),
    },
    {
        "role": "assistant",
        "content": (
            "Kürk Mantolu Madonna stokta bulunmaktadır. "
            "Fiyatı 120 TL, güncel stok sayısı 8'dir."
        ),
    },
]


rendered_chat = template.render(
    bos_token="<s>",
    messages=messages,
    tools=tools,
    add_generation_prompt=False,
)

print("OLUŞTURULAN CHAT TEMPLATE ÇIKTISI")
print("=" * 60)
print(rendered_chat)
