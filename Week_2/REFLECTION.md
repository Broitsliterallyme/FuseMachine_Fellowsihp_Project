# Twelve-Factor App Reflection

## Factor III: Config — Why .env is better than hardcoding passwords

Storing database credentials directly in code is dangerous because the code often ends up
in version control (e.g., GitHub), making secrets publicly visible. A `.env` file keeps
sensitive values — like `POSTGRES_PASSWORD` — out of the codebase entirely. It also means
you can have a weak dev password locally and a strong production password on the server,
with zero code changes. Developers share the codebase but never share the secrets file.
This separation of config from code is the heart of Factor III.

## Factor IV: Backing Services — Why the database is a separate service

Treating the PostgreSQL database as an attached resource (a backing service) means the
application talks to it over a URL, not by embedding the database engine inside the app.
In our Docker Compose setup, the `db` service is independent of the `api` service. This
loose coupling means we can swap PostgreSQL for MySQL or SQLite by changing a single
`DATABASE_URL` variable, without touching application logic. It also means the database
can be scaled, replaced, or restarted independently — essential for production resilience.

## Factor X: Dev/Prod Parity — How Docker keeps environments consistent

Docker packages the application and its dependencies into an image that runs identically
on a developer's laptop, a CI server, and a production machine. Without Docker,
differences in OS versions, Python versions, or library installations often cause bugs that
only appear in production. With Docker Compose, the same `docker-compose.yml` spins up
the exact same PostgreSQL version and app environment everywhere, eliminating the classic
"it works on my machine" problem. This parity makes deployments predictable and safe.
