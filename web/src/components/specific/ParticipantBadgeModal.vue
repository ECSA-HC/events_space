<template>
  <div
    v-if="visible"
    class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-3"
    @click.self="close"
  >
    <div class="w-full max-w-xs bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden" style="max-height:92vh;">

      <!-- Header bar -->
      <div class="flex items-center justify-between px-4 py-2.5 border-b border-gray-100 flex-shrink-0">
        <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Badge Preview</span>
        <button class="text-gray-400 hover:text-black transition" @click="close">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Badge (A4 aspect ratio, scrollable) -->
      <div class="overflow-y-auto flex-1">
        <!-- container-type allows cqw font sizing -->
        <div ref="badgeRef" class="relative w-full" style="aspect-ratio:210/297;container-type:inline-size;background:#eae7df;">

          <!-- ── Logos ────────────────────────────────────────────── -->
          <div class="absolute flex justify-between items-center"
               style="top:3%;left:3.5%;right:3.5%;height:6.2%;">
            <img src="@/assets/ecsalogo.png"  class="h-full w-auto object-contain" alt="ECSA" />
            <img src="@/assets/mauritius.png" class="h-full w-auto object-contain" alt="Logo" />
          </div>

          <!-- ── Event title line 1 (orange) ─────────────────────── -->
          <div class="absolute w-full text-center font-bold leading-tight px-2"
               style="top:16%;transform:translateY(-50%);color:#F7941D;font-size:3.8cqw;">
            {{ title1 }}
          </div>

          <!-- ── Event title line 2 (teal) ──────────────────────── -->
          <div class="absolute w-full text-center font-bold leading-tight px-2"
               style="top:20.5%;transform:translateY(-50%);color:#0095B6;font-size:3.4cqw;">
            {{ title2 }}
          </div>

          <!-- ── Dates & location ────────────────────────────────── -->
          <div class="absolute w-full text-center font-semibold px-3"
               style="top:25.3%;transform:translateY(-50%);color:#222;font-size:1.6cqw;">
            {{ dateStr }}
          </div>

          <!-- ── THEME box + text ────────────────────────────────── -->
          <div class="absolute flex items-center justify-center font-bold"
               style="top:29.4%;left:3.5%;width:11%;height:2.5%;background:#00AEEF;color:#fff;font-size:1.4cqw;">
            THEME:
          </div>
          <div class="absolute font-semibold px-3 leading-snug"
               style="top:34%;left:3.5%;right:3.5%;color:#111;font-size:1.5cqw;">
            {{ theme }}
          </div>

          <!-- ── Role banner ─────────────────────────────────────── -->
          <div
            class="absolute w-full flex items-center justify-center font-black"
            :style="{
              top: '48.1%',
              height: '9.4%',
              background: roleColor,
              color: roleBannerTextColor,
              fontSize: roleFontSize,
              letterSpacing: '0.04em',
            }"
          >
            {{ roleLabel }}
          </div>

          <!-- ── Info rows ───────────────────────────────────────── -->
          <template v-for="(row, i) in infoRows" :key="i">
            <div class="absolute flex"
                 :style="{ top: rowTops[i], left: '3.5%', right: '3.5%', height: '4.6%' }">
              <!-- Label cell -->
              <div class="flex items-center justify-center font-bold shrink-0"
                   :style="{ width:'18%', background: roleColor, color: roleBannerTextColor, fontSize:'1.4cqw' }">
                {{ row.label }}
              </div>
              <!-- Content cell -->
              <div class="flex items-center flex-1 px-1 font-semibold truncate"
                   :style="{ background: roleLightColor, color:'#111', fontSize:'1.5cqw' }">
                {{ row.value }}
              </div>
            </div>
          </template>

          <!-- ── QR code ─────────────────────────────────────────── -->
          <div class="absolute flex flex-col items-center"
               style="top:79%;left:50%;transform:translateX(-50%);width:13%;">
            <img :src="qrUrl" alt="QR" class="w-full h-auto" />
            <span class="text-center mt-0.5" style="font-size:1.1cqw;color:#888;white-space:nowrap;">
              Scan to confirm attendance
            </span>
          </div>

          <!-- ── Flag strip ──────────────────────────────────────── -->
          <div class="absolute w-full flex justify-center items-center gap-px"
               style="bottom:1.5%;height:3.4%;">
            <img v-for="code in flagCodes" :key="code"
                 :src="`https://flagcdn.com/40x30/${code}.png`"
                 :alt="code"
                 class="h-full w-auto object-contain" />
          </div>

        </div>
      </div>

      <!-- Download button -->
      <div class="flex-shrink-0 px-4 py-3 border-t border-gray-100 flex justify-center bg-white">
        <button
          @click="downloadPDF"
          class="bg-[#0095B6] hover:bg-[#007a95] text-white px-6 py-2 rounded-full text-sm font-semibold transition"
        >
          Download Badge PDF
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import html2pdf from 'html2pdf.js'

const props = defineProps({
  visible: Boolean,
  user:    Object,   // participant from event participants list
  event:   Object,   // full event object
})

const emit = defineEmits(['close'])
const close = () => emit('close')

const badgeRef = ref(null)

// ── Role colour map ──────────────────────────────────────────────────────────
const ROLE_COLORS = {
  media:        '#FFD700',
  moderator:    '#F7941D',
  secretariat:  '#00AEEF',
  speaker:      '#C8102E',
  presenter:    '#C8102E',
  delegate:     '#009639',
  moh:          '#009639',
  member_state: '#009639',
  other_africa: '#009639',
  world:        '#009639',
  student:      '#009639',
  participant:  '#009639',
  exhibitor:    '#F7941D',
  sponsor:      '#F7941D',
}
const ROLE_LABELS = {
  media:        'MEDIA',
  moderator:    'MODERATOR',
  secretariat:  'SECRETARIAT',
  speaker:      'SPEAKER',
  presenter:    'PRESENTER',
  delegate:     'DELEGATE',
  moh:          'DELEGATE',
  member_state: 'DELEGATE',
  other_africa: 'DELEGATE',
  world:        'DELEGATE',
  student:      'STUDENT',
  participant:  'PARTICIPANT',
  exhibitor:    'EXHIBITOR',
  sponsor:      'SPONSOR',
}

const roleKey = computed(() => {
  const r = props.user?.participation_role
  if (!r) return 'delegate'
  // enum object {name, value} or plain string
  return (typeof r === 'object' ? r.name : String(r)).toLowerCase()
})

const roleColor         = computed(() => ROLE_COLORS[roleKey.value] || '#0095B6')
const roleLabel         = computed(() => ROLE_LABELS[roleKey.value] || roleKey.value.toUpperCase())
const roleBannerTextColor = computed(() => roleColor.value === '#FFD700' ? '#000' : '#fff')
const roleLightColor    = computed(() => {
  const hex = roleColor.value.replace('#', '')
  const r = parseInt(hex.slice(0,2),16)/255
  const g = parseInt(hex.slice(2,4),16)/255
  const b = parseInt(hex.slice(4,6),16)/255
  const lr = Math.round((0.80 + r*0.20)*255)
  const lg = Math.round((0.80 + g*0.20)*255)
  const lb = Math.round((0.80 + b*0.20)*255)
  return `rgb(${lr},${lg},${lb})`
})

// Dynamic font size for role banner (mirrors Python: max(32,min(64,490//len)))
const roleFontSize = computed(() => {
  const label = roleLabel.value
  const sizePt = Math.max(32, Math.min(64, Math.floor(490 / Math.max(label.length, 1))))
  // pt to cqw: 1pt = 0.353mm, 1mm = (100/210)cqw ≈ 0.476cqw
  return `${(sizePt * 0.353 * 0.476).toFixed(2)}cqw`
})

// ── Event title split ────────────────────────────────────────────────────────
const normalizedName = computed(() => {
  const name = props.event?.event || ''
  return name
    .replace(/ᵗʰ/g,'th').replace(/ˢᵗ/g,'st').replace(/ⁿᵈ/g,'nd').replace(/ʳᵈ/g,'rd')
})
const title1 = computed(() => {
  const parts = normalizedName.value.split(' & ')
  if (parts.length >= 2) return parts[0].trim()
  const words = normalizedName.value.split(' ')
  return words.slice(0, Math.ceil(words.length / 2)).join(' ')
})
const title2 = computed(() => {
  const parts = normalizedName.value.split(' & ')
  if (parts.length >= 2) return '& ' + parts.slice(1).join(' & ').trim()
  const words = normalizedName.value.split(' ')
  return words.slice(Math.ceil(words.length / 2)).join(' ')
})

// ── Dates ────────────────────────────────────────────────────────────────────
function fmtDate(d) {
  if (!d) return ''
  const dt = new Date(d)
  return dt.toLocaleDateString('en-GB', { day:'numeric', month:'long', year:'numeric' })
}
const dateStr = computed(() => {
  const s = fmtDate(props.event?.start_date)
  const e = fmtDate(props.event?.end_date)
  const loc = props.event?.location || ''
  const range = s && e ? `${s} – ${e}` : (s || e)
  return [range, loc].filter(Boolean).join('  |  ')
})

const theme = computed(() => props.event?.theme || '')

// ── Info rows ─────────────────────────────────────────────────────────────────
const infoRows = computed(() => [
  { label: 'Name',         value: [props.user?.firstname, props.user?.lastname].filter(Boolean).join(' ') },
  { label: 'Organisation', value: props.user?.organisation || '' },
  { label: 'Country',      value: props.user?.country || '' },
])
// top positions (% of badge height) matching PDF layout: 59.3%, 65.5%, 71.7%
const rowTops = ['59.3%', '65.5%', '71.7%']

// ── QR code ──────────────────────────────────────────────────────────────────
const apiOrigin = import.meta.env.VITE_CLIENT_ORIGIN || 'https://events.ecsahc.org'
const qrUrl = computed(() => {
  const regId = props.user?.id
  const eventId = props.event?.id
  const data = `${apiOrigin}/event-attendance/${eventId}?reg=${regId}`
  return `https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=${encodeURIComponent(data)}`
})

// ── ECSA member-state flags ───────────────────────────────────────────────────
const flagCodes = ['sz', 'ke', 'ls', 'mw', 'mu', 'tz', 'ug', 'zm', 'zw']

// ── PDF download ──────────────────────────────────────────────────────────────
function downloadPDF() {
  if (!badgeRef.value) return
  const name = [props.user?.firstname, props.user?.lastname].filter(Boolean).join('_') || 'badge'
  html2pdf()
    .set({
      margin: 0,
      filename: `badge_${name}.pdf`,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 3, useCORS: true },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
    })
    .from(badgeRef.value)
    .save()
}
</script>
