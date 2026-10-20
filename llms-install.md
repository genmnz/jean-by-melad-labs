# Installing Jean (for AI agents)

Jean is a **remote** MCP server. There is nothing to download, build or run, and no API key.

1. Add a remote MCP server named `jean` with the URL `https://jeanslabs.vercel.app/mcp`
   (transport: Streamable HTTP; authentication: none).
2. For clients configured by JSON, the entry is:

   ```json
   { "mcpServers": { "jean": { "url": "https://jeanslabs.vercel.app/mcp" } } }
   ```

3. Verify: call `find_restriction_sites` with
   `{"$subject": {"sequence": "GGATCCAAAA"}, "enzymes": ["BamHI"]}`. It returns BamHI cutting
   the sequence; any error means the server was not added.

Tools take the molecule to act on as `$subject` (a sequence, an accession, or a file). The server is
stateless, so pass it with every call. Field-by-field help: https://jeanslabs.vercel.app/docs/api/mcp
