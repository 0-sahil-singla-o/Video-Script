# Social Media Distribution Copy: Shopify SKIP LOCKED Explainer

---

## 1. Instagram Reels
**Hook:**
When two people click buy on the last hoodie at the exact same millisecond... who wins?

**Caption:**
If your flash sale gets hit by 100,000 checkouts at once, standard database locking creates a brutal traffic jam.

Here is the exact trick Shopify uses to stop selling the last hoodie twice without slowing down checkouts:

Tokens in a bowl.

Instead of 1 row with a counter that says "6 left", create 6 separate rows (1 per physical hoodie). Then use `SELECT ... FOR UPDATE SKIP LOCKED`.

Now every checkout grabs a free token and skips right past occupied ones. Zero waiting, zero overselling.

Save this for your next system design interview. ⚡

#systemdesign #backend #softwareengineering #webdevelopment #database #coding #redis #mysql

---

## 2. X (Twitter) Thread
**Post 1 (Hook):**
How does Shopify stop selling the last hoodie twice during a massive flash sale?

Standard database locks lock the whole row and cause a traffic jam.

Here’s the simple trick: Tokens in a bowl. 🧵👇

**Post 2 (Architecture):**
Instead of having 1 inventory row with `quantity = 6`, Shopify splits it into 6 individual rows—one for every single physical item.

Think of it like 6 poker chips in a glass bowl.

**Post 3 (The SQL Magic):**
When a buyer hits checkout, the query doesn't wait in line. It runs:
`SELECT id FROM inventory WHERE item_id = 123 AND status = 'available' LIMIT 1 FOR UPDATE SKIP LOCKED`

If another checkout is already locking token #1, your transaction simply skips to token #2.

No queue. No deadlocks. 100% accurate inventory.

---

## 3. LinkedIn Post
**Headline:** How Shopify solved the "Last Hoodie Problem" without breaking database throughput.

In high-concurrency systems, flash sales are an inventory nightmare.

If 10,000 customers try to purchase the last remaining item at the exact same millisecond:
- Traditional locks (`SELECT ... FOR UPDATE`) serialize the queue, causing latency spikes and connection timeouts.
- Optimistic locking leads to high transaction abort rates.

Shopify’s elegant pattern: **The Token Bowl pattern.**

Instead of maintaining a single row with an integer counter (`remaining: 6`), you model the inventory as atomic token rows (6 distinct rows in a table).

When checking out:
Each worker queries with `SKIP LOCKED`. If row #1 is locked by an ongoing transaction, the database engine skips right past it and acquires row #2 in microseconds.

**The takeaway:**
When row-level contention becomes your bottleneck, change the grain of your data. De-aggregate hot rows into discrete tokens.
