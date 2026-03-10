
🗺️ The Refined "Complete" Roadmap

### Phase 3.5: The Backend Core (Finishing Now)
- **Identity Logic:** Implement the `get_current_user` dependency to retrieve the user from the database and resolve their `role_name`.
- **Chat Endpoint:** Build `POST /chat/send` to connect the user's message and their database role to the `app_graph`.
- **Chat Persistence:** Introduce a `chat_history` table in PostgreSQL to ensure messages are retained when the user refreshes their (future) React app.
- **Admin Upload Logic:** Finalize the `POST /ingest` endpoint with a role check, restricting access to users with `role_id == 1`.

### Phase 4: Security & Authentication (The "Fancy" Part)
- **JWT Implementation:** Establish the login flow — `POST /auth/login` returns a JWT token.
- **Password Hashing:** Ensure user passwords are stored securely using `passlib`, never in plain text.
- **Token-to-Graph:** Update the chat endpoint to extract the `user_role` directly from the decrypted JWT.

### Phase 5: The React "Enterprise" Frontend
- **Layout:** Design a sidebar (history panel), a main chat area, and an admin dashboard.
- **State Management:** Use the Context API or Redux to store the user's role and token.
- **Dynamic UI:**
  - If `role == 'admin'`, display the **Upload PDF** button.
  - If `role == 'analyst'`, display a **SQL Query Preview** toggle.