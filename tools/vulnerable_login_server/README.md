# 🕵️ Vulnerable Login Server – Writeup

## Target Info
- IP: 127.0.0.1
- Port: 9090
- Service: Custom TCP Login Server

---

## 🧩 Step 1: Enumeration

Using `netcat`:

nc 127.0.0.1 9090

We find a basic login prompt. No rate limiting or CAPTCHA.

---

## 🧪 Step 2: Hash Reversal

After inspecting `server.py`, we find the password is stored as an **MD5 hash**.

We reverse the hash using `crackstation.net` or a local wordlist.  
The password is `password123`.

---

## 🚀 Step 3: Login and Get the Flag

Using the credentials `admin:password123`, we get:

Login successful! FLAG: THM{simple_ctf_but_realistic}


---

## 🧠 Lessons Learned

- Hashes are not secure without salting.
- Always use slow hash algorithms like bcrypt or Argon2 for credentials.
- Code review reveals critical logic flaws.

---

## 🔧 Bonus

Patch the server to:
- Use salted hashes
- Add lockout after failed attempts
