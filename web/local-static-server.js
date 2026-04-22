const http = require("http");
const fs = require("fs");
const path = require("path");

const root = __dirname;
const port = 8080;

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".webmanifest": "application/manifest+json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".ico": "image/x-icon",
  ".txt": "text/plain; charset=utf-8"
};

function send(res, status, body, type = "text/plain; charset=utf-8") {
  res.writeHead(status, { "Content-Type": type });
  res.end(body);
}

function resolvePath(urlPath) {
  const clean = decodeURIComponent(urlPath.split("?")[0]);
  let target = path.normalize(path.join(root, clean));
  if (!target.startsWith(root)) return null;

  if (fs.existsSync(target) && fs.statSync(target).isDirectory()) {
    target = path.join(target, "index.html");
  }
  if (!fs.existsSync(target) && clean === "/") {
    target = path.join(root, "index.html");
  }
  return target;
}

http.createServer((req, res) => {
  const target = resolvePath(req.url || "/");
  if (!target) {
    send(res, 403, "Forbidden");
    return;
  }
  if (!fs.existsSync(target)) {
    send(res, 404, "Not found");
    return;
  }

  fs.readFile(target, (error, data) => {
    if (error) {
      send(res, 500, "Server error");
      return;
    }
    const ext = path.extname(target).toLowerCase();
    send(res, 200, data, mimeTypes[ext] || "application/octet-stream");
  });
}).listen(port, "127.0.0.1", () => {
  console.log(`RECOVS static server running at http://127.0.0.1:${port}`);
});
