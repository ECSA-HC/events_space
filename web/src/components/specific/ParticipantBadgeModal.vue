<template>
  <div
    v-if="visible"
    class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-3"
    @click.self="close"
  >
    <div class="w-full max-w-lg bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden" style="max-height:95vh;">

      <!-- Header bar -->
      <div class="flex items-center justify-between px-4 py-2.5 border-b border-gray-100 flex-shrink-0">
        <span class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Badge Preview</span>
        <button class="text-gray-400 hover:text-black transition" @click="close">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Badge (A6 = 105×148mm, same aspect ratio as A4) -->
      <div class="flex-1 flex items-center justify-center p-2 bg-gray-50">
        <div
          ref="badgeRef"
          class="relative w-full"
          :style="{
            aspectRatio: '105/148',
            containerType: 'inline-size',
            backgroundImage: `url(${badgeBg})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            fontFamily: '\'Roboto Condensed\', Roboto, Arial, sans-serif',
          }"
        >

          <!-- ── Logos ─────────────────────────────────────────────────── -->
          <!-- Left: Eswatini MoH  5–32 mm | Right: ECSA-HC  58–98 mm      -->
          <!-- Enlarged to 13% height for better visibility                 -->
          <div class="absolute flex justify-between items-center"
               style="top:1.5%;left:3%;right:1.5%;height:13%;">
            <img src="@/assets/moh_sz.png"         class="h-full w-auto object-contain" style="max-width:48%;" alt="Kingdom of Eswatini Ministry of Health" />
            <img src="@/assets/ecsa_hc_banner.png" class="h-full w-auto object-contain" style="max-width:48%;" alt="ECSA-HC" />
          </div>

          <!-- ── Title 1 (orange) baseline at y≈22% of badge height ────── -->
          <div class="absolute w-full text-center leading-tight px-2"
               style="top:22%;transform:translateY(-50%);color:#F7941D;font-size:7.1cqw;font-weight:900;font-family:'Roboto Condensed',Roboto,sans-serif;">
            {{ title1 }}
          </div>

          <!-- ── Title 2 (dark/near-black) baseline at y≈28% ──────────── -->
          <div class="absolute w-full text-center leading-tight px-2"
               style="top:28%;transform:translateY(-50%);color:#111111;font-size:6.1cqw;font-weight:900;font-family:'Roboto Condensed',Roboto,sans-serif;">
            {{ title2 }}
          </div>

          <!-- ── Dates & location at y≈33.5% ──────────────────────────── -->
          <div class="absolute w-full text-center px-3"
               style="top:33.5%;transform:translateY(-50%);color:#222;font-size:2.6cqw;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
            {{ dateStr }}
          </div>

          <!-- ── THEME box ─────────────────────────────────────────────── -->
          <div class="absolute flex items-center justify-center"
               style="top:38%;left:9.4%;width:17.3%;height:3.7%;background:#00AEEF;color:#fff;font-size:3.5cqw;font-weight:900;">
            THEME:
          </div>
          <!-- Theme text -->
          <div class="absolute leading-snug"
               style="top:42.5%;left:9.7%;right:3%;color:#111;font-size:3.2cqw;font-weight:700;">
            {{ theme }}
          </div>

          <!-- ── Role banner  top=52%, height=8.3%, left/right=5.7% (widened to match PDF) ─ -->
          <div
            class="absolute flex items-center justify-center"
            :style="{
              top: '52%',
              left: '5.7%',
              right: '5.7%',
              height: '8.3%',
              background: roleColor,
              color: roleBannerTextColor,
              fontSize: roleFontSize,
              fontWeight: 900,
              fontFamily: '\'Roboto Condensed\', Roboto, sans-serif',
              letterSpacing: '0.06em',
            }"
          >
            {{ roleLabel }}
          </div>

          <!-- ── Info rows (Name / Designation / Organization) ──────────── -->
          <template v-for="(row, i) in infoRows" :key="i">
            <div class="absolute flex overflow-hidden"
                 :style="{ top: rowTops[i], left:'5.7%', right:'5.7%', height:'4.5%' }">
              <!-- Label -->
              <div
                class="flex items-center justify-center shrink-0 text-center"
                :style="{ width: row.labelPct, background:'#00AEEF', color:'#fff', fontSize:row.labelFontSize, fontWeight:700 }"
              >
                {{ row.label }}
              </div>
              <!-- Value -->
              <div
                class="flex items-center flex-1 min-w-0 px-1 truncate"
                :style="{ background: roleLightColor, color:'#111', fontSize:row.valueFontSize, fontWeight:600 }"
              >
                {{ row.value }}
              </div>
            </div>
          </template>

          <!-- ── QR code  top=79%, width=15% centred ─────────────────── -->
          <div class="absolute flex flex-col items-center"
               style="top:79%;left:50%;transform:translateX(-50%);width:15%;">
            <img :src="qrUrl" alt="QR" class="w-full h-auto" />
            <span class="text-center mt-0.5" style="font-size:1.4cqw;color:#666;white-space:nowrap;">
              Scan to confirm attendance
            </span>
          </div>

          <!-- ── Flag strip  top=93%, single row ─────────────────────── -->
          <div class="absolute flex justify-center items-center"
               style="top:93%;left:4%;right:4%;height:5%;gap:0.4cqw;overflow:hidden;">
            <img v-for="code in flagCodes" :key="code"
                 :src="`https://flagcdn.com/40x30/${code}.png`"
                 :alt="code" style="height:100%;width:auto;object-fit:contain;flex-shrink:1;min-width:0;" />
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
import api from '@/plugins/axios'
import badgeBg from '@/assets/badge_bg.jpg'

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
  return (typeof r === 'object' ? r.name : String(r)).toLowerCase()
})

const roleColor           = computed(() => ROLE_COLORS[roleKey.value] || '#0095B6')
const roleLabel           = computed(() => ROLE_LABELS[roleKey.value] || roleKey.value.toUpperCase())
const roleBannerTextColor = computed(() => roleColor.value === '#FFD700' ? '#000' : '#fff')
const roleLightColor      = computed(() => {
  const hex = roleColor.value.replace('#', '')
  const r   = parseInt(hex.slice(0,2), 16) / 255
  const g   = parseInt(hex.slice(2,4), 16) / 255
  const b   = parseInt(hex.slice(4,6), 16) / 255
  return `rgb(${Math.round((0.80+r*0.20)*255)},${Math.round((0.80+g*0.20)*255)},${Math.round((0.80+b*0.20)*255)})`
})

// Banner font size: matches Python formula max(18,min(30,330//len)) converted to cqw
// 1pt = 0.353mm; container = 105mm → 1cqw = 1.05mm → 1pt ≈ 0.336cqw
const roleFontSize = computed(() => {
  const fsize = Math.max(18, Math.min(30, Math.floor(330 / Math.max(roleLabel.value.length, 1))))
  return `${(fsize * 0.336).toFixed(2)}cqw`
})

// Shrinks a font size (pt) down toward floorPt until `text` is estimated to fit
// widthMm — mirrors the Python _shrink_to_fit stringWidth loop, using an
// average-char-width approximation since canvas.measureText isn't practical
// against cqw units here. Returns cqw for direct use in inline styles.
function fitFontSizeCqw(text, startPt, floorPt, widthMm) {
  const avgCharMm = (pt) => pt * 0.3528 * 0.55
  let pt = startPt
  while (pt > floorPt && text.length * avgCharMm(pt) > widthMm) {
    pt -= 0.5
  }
  return `${(pt * 0.336).toFixed(2)}cqw`
}

// Generic word abbreviations for organization names too long to fit even at
// the smallest readable font (must match ORG_ABBREVIATIONS in events.py).
// Long country/region names go first since they're multi-word phrases.
const ORG_ABBREVIATIONS = [
  [/\bUnited Kingdom\b/gi, 'UK'], [/\bUnited States of America\b/gi, 'USA'],
  [/\bUnited States\b/gi, 'US'], [/\bUnited Arab Emirates\b/gi, 'UAE'],
  [/\bDemocratic Republic of (the )?Congo\b/gi, 'DRC'],
  [/\bUniversity\b/gi, 'Univ.'], [/\bInstitute\b/gi, 'Inst.'],
  [/\bDepartment\b/gi, 'Dept.'], [/\bMinistry\b/gi, 'Min.'],
  [/\bInternational\b/gi, "Int'l"], [/\bOrgani[sz]ation\b/gi, 'Org.'],
  [/\bAssociation\b/gi, 'Assoc.'], [/\bFoundation\b/gi, 'Fdn.'],
  [/\bCorporation\b/gi, 'Corp.'], [/\bCompany\b/gi, 'Co.'],
  [/\bLimited\b/gi, 'Ltd.'], [/\bGovernment\b/gi, 'Govt.'],
  [/\bNational\b/gi, 'Natl.'], [/\bRegional\b/gi, "Reg'l"],
  [/\bProgramme\b/gi, 'Prog.'], [/\bProgram\b/gi, 'Prog.'],
  [/\bManagement\b/gi, 'Mgmt.'], [/\bDevelopment\b/gi, 'Dev.'],
  [/\bCommunity\b/gi, 'Cmty.'], [/\bRepublic\b/gi, 'Rep.'],
  [/\bAfrican\b/gi, 'Afr.'], [/\bSouthern\b/gi, 'S.'],
  [/\bEastern\b/gi, 'E.'], [/\bWestern\b/gi, 'W.'],
  [/\bNorthern\b/gi, 'N.'], [/\bCentral\b/gi, 'Ctrl.'],
  [/\bHealth\b/gi, 'Hlth'], [/\bServices\b/gi, 'Svcs'],
  [/\bAgency\b/gi, 'Agcy'], [/\bAuthority\b/gi, 'Auth.'],
  [/\bCommission\b/gi, 'Comm.'], [/\bResearch\b/gi, 'Rsch'],
  [/\bTechnology\b/gi, 'Tech.'], [/\bAdministration\b/gi, 'Admin.'],
]
// Words skipped when generating an initials-based acronym fallback (e.g.
// "University College London" -> "UCL") for orgs with no "(ACRONYM)" of
// their own (must match ORG_STOPWORDS in events.py).
const ORG_STOPWORDS = new Set(['and', 'of', 'for', 'the', 'in', 'on', 'at', 'a', 'an', '&', 'to'])

function abbreviateOrgWords(text) {
  let out = text
  for (const [pattern, repl] of ORG_ABBREVIATIONS) out = out.replace(pattern, repl)
  return out
}

function generateOrgAcronym(text) {
  const commaIdx = text.indexOf(',')
  let main = commaIdx === -1 ? text : text.slice(0, commaIdx)
  const suffix = (commaIdx === -1 ? '' : text.slice(commaIdx + 1)).trim()
  main = main.replace(/\([^)]*\)/g, '')
  const words = main.match(/[A-Za-z']+/g) || []
  const initials = words.filter(w => !ORG_STOPWORDS.has(w.toLowerCase())).map(w => w[0].toUpperCase()).join('')
  if (initials.length < 2) return null
  return suffix ? `${initials}, ${suffix}` : initials
}

// Mirrors events.py's _smart_shorten_org: try the original, the org's own
// acronym (if spelled out in parentheses), generic word abbreviation, both
// combined, and a generated initials acronym — and use whichever form fits
// at the LARGEST font size, not just whichever fits at the smallest. Falls
// back to an ellipsis only if nothing fits even at the floor size.
function smartShortenOrg(text, startPt, floorPt, widthMm) {
  const fits = (t, pt) => t.length * (pt * 0.3528 * 0.55) <= widthMm
  const sizeFor = (t) => {
    let pt = startPt
    while (pt > floorPt && !fits(t, pt)) pt -= 0.5
    return pt
  }

  const candidates = [text]
  const m = text.match(/\(([A-Z]{2,12})\)\s*,?\s*(.*)$/)
  let acronymForm = null
  if (m) {
    const rest = m[2].trim().replace(/^,\s*/, '')
    acronymForm = rest ? `${m[1]}, ${rest}` : m[1]
    candidates.push(acronymForm)
  }
  const abbreviated = abbreviateOrgWords(text)
  if (abbreviated !== text) candidates.push(abbreviated)
  if (acronymForm) {
    const abbreviatedAcronym = abbreviateOrgWords(acronymForm)
    if (abbreviatedAcronym !== acronymForm) candidates.push(abbreviatedAcronym)
  }
  const generated = generateOrgAcronym(text)
  if (generated && !candidates.includes(generated)) candidates.push(generated)

  let bestCand = text, bestSize = floorPt, bestFits = false, bestScore = -1
  for (const cand of candidates) {
    const size = sizeFor(cand)
    const candFits = fits(cand, size)
    const score = candFits ? size : -1
    if (score > bestScore) {
      bestScore = score; bestCand = cand; bestSize = size; bestFits = candFits
    }
  }
  if (bestFits) return { value: bestCand, fontSize: `${(bestSize * 0.336).toFixed(2)}cqw` }

  const shortest = candidates.reduce((a, b) => (b.length < a.length ? b : a))
  let truncated = shortest
  while (truncated.length && !fits(truncated + '…', floorPt)) truncated = truncated.slice(0, -1)
  return { value: `${truncated.replace(/[\s,]+$/, '')}…`, fontSize: `${(floorPt * 0.336).toFixed(2)}cqw` }
}

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
  return new Date(d).toLocaleDateString('en-GB', { day:'numeric', month:'long', year:'numeric' })
}
const dateStr = computed(() => {
  const s   = fmtDate(props.event?.start_date)
  const e   = fmtDate(props.event?.end_date)
  const loc = props.event?.location || ''
  const range = s && e ? `${s} – ${e}` : (s || e)
  return [range, loc].filter(Boolean).join('  |  ')
})

const theme = computed(() => props.event?.theme || '')

// ── Info rows with variable label widths matching the PDF layout ───────────────
// Row spans 5.7%–94.3% of the 105mm page (93mm wide, matching events.py's
// ROW_X0/ROW_X1=6.0/99.0). Label widths below are that same mm split
// (Name 22.0mm, Designation 34.5mm, Organization 34.9mm) expressed as a
// percentage of the row's own 93mm width. Value/label font sizes shrink to
// fit long text the same way the PDF does, falling back to the existing
// `truncate` (ellipsis) class for anything still too long.
const ROW_WIDTH_MM = 93.0
const infoRows = computed(() => {
  const title = (props.user?.title || '').trim().replace(/\.$/, '')
  const first = props.user?.firstname || ''
  const last  = props.user?.lastname  || ''
  const displayName = title ? `${title}. ${first} ${last}` : [first, last].filter(Boolean).join(' ')

  const specs = [
    { label: 'Name',         value: displayName,                    labelMm: 22.0, contentMm: 71.0 },
    { label: 'Designation',  value: props.user?.position     || '', labelMm: 34.5, contentMm: 58.5 },
    { label: 'Organization', value: props.user?.organisation || '', labelMm: 34.9, contentMm: 58.1 },
  ]
  return specs.map(s => {
    const labelFontSize = fitFontSizeCqw(s.label, 12, 9, s.labelMm - 2)
    const labelPct = `${((s.labelMm / ROW_WIDTH_MM) * 100).toFixed(2)}%`
    if (s.label === 'Organization') {
      const fit = smartShortenOrg(s.value, 11, 7, s.contentMm - 3)
      return { label: s.label, value: fit.value, labelPct, labelFontSize, valueFontSize: fit.fontSize }
    }
    return {
      label: s.label,
      value: s.value,
      labelPct,
      labelFontSize,
      valueFontSize: fitFontSizeCqw(s.value, 11, 7, s.contentMm - 3),
    }
  })
})

// Row top positions — shifted slightly to match enlarged logo area
const rowTops = ['62%', '68%', '74%']

// ── QR code ──────────────────────────────────────────────────────────────────
const apiOrigin = 'https://events.ecsahc.org'
const qrUrl = computed(() => {
  const data = `${apiOrigin}/event-attendance/${props.event?.id}?reg=${props.user?.id}`
  return `https://api.qrserver.com/v1/create-qr-code/?size=120x120&data=${encodeURIComponent(data)}`
})

// ── ECSA member-state flags ───────────────────────────────────────────────────
const flagCodes = ['sz', 'ke', 'ls', 'mw', 'mu', 'mz', 'st', 'tz', 'ug', 'zm', 'zw']

// ── PDF download — calls the backend which generates a proper A6 PDF ─────────
async function downloadPDF() {
  const eventId = props.event?.id
  const userId  = props.user?.user_id   // registration.user_id from the event participants list
  if (!eventId || !userId) {
    console.warn('Badge download: missing eventId or userId', { eventId, userId, user: props.user })
    alert('Cannot determine participant — please refresh and try again.')
    return
  }
  try {
    const url = `/events/${eventId}/participants/badges?paid=all&user_id=${userId}`
    const response = await api.get(url, { responseType: 'blob' })
    const name = [props.user?.firstname, props.user?.lastname].filter(Boolean).join('_') || 'badge'
    const blob     = new Blob([response.data], { type: 'application/pdf' })
    const objectUrl = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = objectUrl
    link.download = `badge_${name}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(objectUrl)
  } catch (err) {
    console.error('Badge download failed:', err?.response?.status, err?.response?.data || err)
    alert(`Failed to download badge PDF (${err?.response?.status || 'network error'}).`)
  }
}
</script>
