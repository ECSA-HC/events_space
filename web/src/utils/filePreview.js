// src/utils/filePreview.js
const baseUrl = import.meta.env.VITE_API_BASE_URL

export function fileUrl(path) {
  if (!path) return ''
  if (path.startsWith('http')) return path
  return `${baseUrl}/${path.replace(/^\//, '')}`
}

export function isImage(path) {
  if (!path) return false
  return /\.(jpg|jpeg|png|gif|webp)$/i.test(path)
}

export function isPdf(path) {
  return !!path && path.toLowerCase().endsWith('.pdf')
}

export function isOffice(path) {
  if (!path) return false
  return /\.(pptx|ppt|potx)$/i.test(path)
}

// Google Docs Viewer embed — used for pptx/ppt since browsers can't render
// Office files natively. The file must be reachable over public HTTPS.
export function officeViewerUrl(path) {
  return `https://docs.google.com/gview?url=${encodeURIComponent(fileUrl(path))}&embedded=true`
}
