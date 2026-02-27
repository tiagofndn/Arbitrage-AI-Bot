# Security & Compliance

## Simulation by Default

- All execution is simulated
- No real exchange connections by default
- Connectors are interfaces with mock implementations

## Secrets

- **Never commit** `.env`, API keys, or credentials
- Use environment variables or a secrets manager
- `.gitignore` excludes `.env` and common secret patterns

## Exchange Compliance

If you implement real connectors (outside this repo):

- **Terms of Service**: Comply with each exchange's ToS
- **Rate limits**: Respect rate limits; do not attempt to evade
- **Sandbox**: Use exchange sandbox/testnets when available

## Regulatory

- This software does not constitute financial advice
- Users are responsible for their own regulatory compliance
- No support for leveraged or margin trading in production

## Reporting Vulnerabilities

See [SECURITY.md](https://github.com/your-org/ai-arb-lab/blob/main/SECURITY.md) in the repository.
