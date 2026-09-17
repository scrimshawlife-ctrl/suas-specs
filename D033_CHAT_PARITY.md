# D033_CHAT_PARITY.md — Chat surface meaning across clients

**Lifecycle:** `draft` / implementation-binding / not a stack bump  
**Stack:** inherits `0.6.0`  
**Parents:** [MVP_REFERENCE.md](MVP_REFERENCE.md) §5 / §9, [MOBILE_SURFACE.md](MOBILE_SURFACE.md) §6.8, [D033_NATIVE_CLIENT_INTEGRATION.md](D033_NATIVE_CLIENT_INTEGRATION.md) §5  
**Gap id:** G-I-31 (implementation catalog; not a D-id)

Chat is a required *navigation destination*. It is not a released messaging product.

## 1. Same meaning on every surface

| Surface | What the Veteran may see |
|---|---|
| HTML `/app/chat` | Authenticated page. State `UNAVAILABLE` with a stated reason. No compose form. No thread list that implies delivery. |
| iOS | If the app keeps a Chat tab to match [MVP_REFERENCE.md](MVP_REFERENCE.md) §5 nav simplicity, that tab renders the same unavailability. It does not open iMessage, a vendor chat SDK, or `/app/chat` in a WebView. |
| Android | Same as iOS. Scaffold copy that says a responder was messaged, dispatched, or is typing is forbidden. |

A surface with no released domain fact behind it renders as unavailable. It does not render as empty, simulated, or “coming soon” in a way that implies a released workflow ([MOBILE_SURFACE.md](MOBILE_SURFACE.md) §6.8).

## 2. What is not released

- Thread identity, message store, typing indicators, read receipts
- `POST` message commands on `/api/v0` or `/app`
- Device push of chat events (`PUSH` stays `FUTURE`)
- Treating QRF `Message` as chat. `Message` appears only with an authorized contact path ([MVP_REFERENCE.md](MVP_REFERENCE.md) §7.2)

`/app/chat/:threadId` is not a product route. A renderer that emits “Open conversation” hrefs invents that route.

## 3. Conservative behavior until a later release

1. Keep the Chat landmark so nav count stays honest.
2. State unavailability in text.
3. Do not add a no-op send handler.
4. Do not persist local draft messages as if they were delivered.
5. Native clients do not call HTML `/app/chat`.

## 4. Non-claims

This file does not open a chat capability, bump the stack, or advance `UI_CONFORMANCE`.
