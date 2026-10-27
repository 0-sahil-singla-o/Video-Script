# Social Copy: What is an IP Address, and How Does DNS Work?

## Instagram Reel / TikTok / YouTube Shorts
**Audio**: Original Voiceover (@code_explains) + Ambient Lo-Fi Tech Bed
**Cover Text**: "How the Internet Actually Works (IP & DNS in 90 Seconds)"

**Caption**:
Every time you type "google.com" and hit enter, an invisible global scavenger hunt happens in 8 milliseconds. ⚡🌐

Here is what really goes down:
1️⃣ Your device needs a destination number: an **IP Address** (like your physical street address).
2️⃣ But humans hate memorizing numbers like `142.250.190.46`. We use domain names.
3️⃣ That's where **DNS** comes in: the ultimate contacts app of the internet.
4️⃣ If your browser doesn't have it saved, a **Recursive Resolver** (your digital librarian) queries:
   • The **Root Server** (points to the right country/TLD)
   • The **TLD Server** (points to the domain's authoritative server)
   • The **Authoritative Server** (hands back the exact IP!)
5️⃣ It sticks an expiring sticky note on your cache (**TTL**), so your second visit is 15x faster!

Hit save 📌 and follow @code_explains to master backend engineering and web architecture visually.

**Hashtags**:
#webdevelopment #dns #networking #softwareengineer #codinglife #computerscience #techexplained #systemdesign #devcommunity #learntocode #backenddev

---

## X (Twitter)
You type "google.com" and a page appears. But how does your computer actually find it?

Here is the exact journey in 5 steps:

1. IP Address = Your device's postal address (IPv4 has ~4.3B, IPv6 has 340 undecillion).
2. DNS = The internet's phone book, mapping human names to computer numbers.
3. The Resolver = A digital librarian running across the globe.
4. The Chain: Root (.) ➔ TLD (.com) ➔ Authoritative Name Server.
5. Caching & TTL: An expiring sticky note that makes visit #2 load in 8ms instead of 120ms.

When you see `DNS_PROBE_FINISHED_NO_INTERNET`? You simply lost contact with the librarian.

Watch the full 3D visual breakdown below 👇

#webdev #systemdesign #programming

---

## LinkedIn
**Ever wondered what actually happens behind the scenes when you type a URL into your browser?**

Most non-technical people assume the browser just magically "knows" where Google or Netflix lives. 

In reality, your computer is making a multi-stage global lookup across three layers of DNS infrastructure in less time than it takes to blink (8 to 120 milliseconds).

Here is the mental model we should teach every computer science beginner:

• **The IP Address (Postal Address)**: Every connected machine needs a unique address to receive packets. IPv4 (4 numbers separated by dots) gave us ~4.3 billion addresses. Because the world ran out, IPv6 expanded this to 340 undecillion.
• **The Router (The Mailroom)**: Your home router manages one public IP for the outside world, translating incoming packets to private IPs inside your local network (NAT).
• **DNS (The Internet's Phone Book)**: Humans remember names; computers demand numbers. DNS bridges that gap.
• **The Resolver (The Digital Librarian)**: When your local cache misses, your recursive resolver visits:
   1. The Root Server (points to `.com`)
   2. The Top-Level Domain (TLD) Server (points to Google's Name Server)
   3. The Authoritative Server (returns `142.250.190.46`)
• **TTL (The Expiring Sticky Note)**: Caching stores the answer locally with a Time-To-Live countdown, ensuring future visits don't repeat the trip.

What was the concept that made networking finally "click" for you? Let me know in the comments!

#SoftwareEngineering #SystemDesign #Networking #WebDevelopment #ComputerScience #TechEducation