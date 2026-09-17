# Chat tab on web, iOS, and Android

**Stack:** `0.6.0`  
**Parents:** [MVP_REFERENCE.md](MVP_REFERENCE.md) §5, [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §6.8

The product keeps a Chat tab so the two-item nav stays simple. There is no released message store.

| Client | What the person sees |
|---|---|
| Web `GET /app/chat` | Signed-in page that says chat is unavailable, with a reason |
| iOS | Same unavailable text if the tab exists |
| Android | Same. Do not say a responder was messaged, is typing, or was dispatched |

There is no compose box, no thread list, no `/app/chat/:id` product route, and no chat SDK. `Message` on a QRF card is not this tab. That control appears only when a contact path already exists.

Do not load `/app/chat` inside a WebView. Do not save local drafts as if they were sent. Do not add a send route that does nothing.
