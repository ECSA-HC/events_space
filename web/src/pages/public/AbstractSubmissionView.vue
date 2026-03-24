<template>
  <div class="min-h-screen bg-gray-50">

    <!-- ─── Hero ──────────────────────────────────────────────────────────────── -->
    <section class="relative overflow-hidden text-white" style="background: linear-gradient(135deg, #0095B6 0%, #007A96 60%, #005F75 100%);">
      <div class="absolute -top-20 -right-20 w-80 h-80 rounded-full opacity-10" style="background: #F7941D;"></div>
      <div class="absolute -bottom-12 -left-12 w-56 h-56 rounded-full opacity-10" style="background: #F7941D;"></div>
      <div class="relative z-10 max-w-5xl mx-auto px-6 py-16 sm:py-24 text-center">
        <div class="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm px-4 py-1.5 rounded-full text-sm font-medium mb-6">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          ECSA-HC 2026
        </div>
        <h1 class="text-4xl sm:text-5xl font-black mb-4 drop-shadow-sm">Abstract Submission Guidelines</h1>
        <p class="text-lg text-white/80 max-w-2xl mx-auto leading-relaxed">
          Submit your original research and contribute to advancing health in East, Central and Southern Africa.
        </p>

        <!-- Status badge -->
        <div class="mt-8 inline-flex items-center gap-3 px-6 py-3 rounded-2xl font-semibold text-sm" style="background-color: #F7941D; color: #fff;">
          <span class="relative flex h-3 w-3">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 bg-white"></span>
            <span class="relative inline-flex rounded-full h-3 w-3 bg-white"></span>
          </span>
          Abstract Submission Window — NOW OPEN
        </div>

        <!-- Deadline pill -->
        <div class="mt-4 flex justify-center gap-4 flex-wrap">
          <div class="inline-flex items-center gap-2 bg-white/10 px-4 py-2 rounded-full text-sm">
            <svg class="w-4 h-4 text-orange-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span>Deadline: <strong>15th June 2026</strong></span>
          </div>
          <div class="inline-flex items-center gap-2 bg-white/10 px-4 py-2 rounded-full text-sm">
            <svg class="w-4 h-4 text-orange-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            <span><a href="mailto:abstracts2019@ecsahc.org" class="underline hover:text-white">abstracts2019@ecsahc.org</a></span>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── Main content ───────────────────────────────────────────────────────── -->
    <div class="max-w-5xl mx-auto px-6 py-12 space-y-10">

      <!-- ─ Call For Abstract ──────────────────────────────────────────────────── -->
      <section class="bg-white rounded-2xl shadow-sm p-8">
        <div class="flex items-center gap-3 mb-5">
          <div class="h-10 w-10 rounded-xl flex items-center justify-center flex-shrink-0" style="background-color: #0095B6;">
            <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-800">Call For Abstract</h2>
        </div>
        <p class="text-gray-600 leading-relaxed mb-5">
          We encourage work that introduces new ideas and concepts, research and its implementation and its usefulness to
          the society. Please read the following guidelines carefully before submitting your abstract:
        </p>
        <ul class="space-y-3">
          <li v-for="item in callForAbstractItems" :key="item" class="flex items-start gap-3 text-gray-600 text-sm leading-relaxed">
            <span class="mt-1.5 h-2 w-2 rounded-full flex-shrink-0" style="background-color: #0095B6;"></span>
            {{ item }}
          </li>
        </ul>
      </section>

      <!-- ─ Scientific Tracks ──────────────────────────────────────────────────── -->
      <section class="bg-white rounded-2xl shadow-sm p-8">
        <div class="flex items-center gap-3 mb-3">
          <div class="h-10 w-10 rounded-xl flex items-center justify-center flex-shrink-0" style="background-color: #F7941D;">
            <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
          </div>
          <div>
            <h2 class="text-2xl font-bold text-gray-800">Abstract Submission Tracks</h2>
            <p class="text-xs text-gray-500 mt-0.5">16<sup>th</sup> Best Practices Forum &amp; 32<sup>nd</sup> DJCC Meeting</p>
          </div>
        </div>

        <!-- Main theme banner -->
        <div class="rounded-xl px-5 py-4 mb-6 border-l-4" style="background-color: #f0f9fb; border-color: #0095B6;">
          <p class="text-xs font-semibold uppercase tracking-wide mb-1" style="color: #0095B6;">Main Theme</p>
          <p class="text-sm font-bold text-gray-800 leading-snug">
            Shaping the Future of Health in the ECSA Region: Advancing Health Security, Innovation &amp; Sustainability
          </p>
        </div>

        <p class="text-gray-600 text-sm mb-6">
          ECSA-HC 2026 welcomes the submission of abstracts for original contribution in the following tracks:
        </p>

        <div class="space-y-5">
          <div
            v-for="group in scientificTracks"
            :key="group.number"
            class="rounded-xl border border-gray-100 overflow-hidden"
          >
            <!-- Main track header -->
            <div class="flex items-start gap-3 px-4 py-3" :style="{ backgroundColor: group.color + '18' }">
              <span class="text-xs font-black px-2 py-0.5 rounded-md text-white flex-shrink-0 mt-0.5"
                :style="{ backgroundColor: group.color }">
                {{ group.number }}
              </span>
              <span class="text-sm font-bold text-gray-800">{{ group.title }}</span>
            </div>
            <!-- Sub-tracks -->
            <ul class="px-4 py-3 space-y-1.5 bg-white">
              <li
                v-for="sub in group.subtracks"
                :key="sub.code"
                class="flex items-start gap-2 text-xs text-gray-600 leading-relaxed"
              >
                <span class="mt-1 h-1.5 w-1.5 rounded-full flex-shrink-0" :style="{ backgroundColor: group.color }"></span>
                <span><strong class="text-gray-700">{{ sub.code }}:</strong> {{ sub.label }}</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- ─ Submitting + Deadline + Reviews (3-col) ───────────────────────────── -->
      <div class="grid gap-6 md:grid-cols-3">

        <!-- Submitting your abstract -->
        <section class="bg-white rounded-2xl shadow-sm p-7">
          <div class="flex items-center gap-2 mb-4">
            <div class="h-8 w-8 rounded-lg flex items-center justify-center flex-shrink-0" style="background-color: #0095B6;">
              <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
            </div>
            <h3 class="font-bold text-gray-800">Submitting Your Abstract</h3>
          </div>
          <p class="text-xs text-gray-500 mb-3">ECSA-HC 2026 reserves the right to reject or alter abstracts based on, but not limited to:</p>
          <ul class="space-y-2">
            <li v-for="item in submittingItems" :key="item" class="flex items-start gap-2 text-xs text-gray-600 leading-relaxed">
              <span class="mt-1.5 h-1.5 w-1.5 rounded-full flex-shrink-0" style="background-color: #F7941D;"></span>
              {{ item }}
            </li>
          </ul>
        </section>

        <!-- Deadline -->
        <section class="bg-white rounded-2xl shadow-sm p-7">
          <div class="flex items-center gap-2 mb-4">
            <div class="h-8 w-8 rounded-lg flex items-center justify-center flex-shrink-0" style="background-color: #F7941D;">
              <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="font-bold text-gray-800">Abstract Deadline</h3>
          </div>
          <div class="bg-orange-50 border border-orange-200 rounded-xl px-4 py-3 mb-3 text-center">
            <p class="text-2xl font-black" style="color: #F7941D;">15th June 2026</p>
            <p class="text-xs text-orange-600 mt-1">Strictly observed</p>
          </div>
          <p class="text-xs text-gray-600 leading-relaxed">
            Abstract deadlines are strictly observed. Only abstracts received by the published deadline (15th June 2026) are guaranteed acceptance.
            Post-deadline abstracts will not be accepted.
          </p>
        </section>

        <!-- Review Process -->
        <section class="bg-white rounded-2xl shadow-sm p-7">
          <div class="flex items-center gap-2 mb-4">
            <div class="h-8 w-8 rounded-lg flex items-center justify-center flex-shrink-0" style="background-color: #0095B6;">
              <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
            </div>
            <h3 class="font-bold text-gray-800">Review Process</h3>
          </div>
          <p class="text-xs text-gray-600 leading-relaxed mb-3">
            An international panel of experts will review the abstracts. Each abstract will be reviewed by at least three different reviewers.
          </p>
          <p class="text-xs text-gray-500 mb-2">Abstracts may be selected for:</p>
          <ul class="space-y-1.5">
            <li class="flex items-center gap-2 text-xs text-gray-600">
              <span class="h-1.5 w-1.5 rounded-full flex-shrink-0" style="background-color: #0095B6;"></span>
              Oral presentation
            </li>
            <li class="flex items-center gap-2 text-xs text-gray-600">
              <span class="h-1.5 w-1.5 rounded-full flex-shrink-0" style="background-color: #F7941D;"></span>
              Poster presentation
            </li>
            <li class="flex items-center gap-2 text-xs text-gray-600">
              <span class="h-1.5 w-1.5 rounded-full flex-shrink-0 bg-red-400"></span>
              Rejection
            </li>
          </ul>
          <div class="mt-3 flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-semibold text-white" style="background-color: #0095B6;">
            <svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            Notification by email before <span class="ml-1 underline">5th July 2026</span>
          </div>
        </section>
      </div>

      <!-- ─ Presentations ──────────────────────────────────────────────────────── -->
      <div class="grid gap-6 md:grid-cols-2">

        <!-- Session Presentations -->
        <section class="bg-white rounded-2xl shadow-sm p-7">
          <div class="flex items-center gap-3 mb-4">
            <div class="h-9 w-9 rounded-xl flex items-center justify-center flex-shrink-0" style="background-color: #0095B6;">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M15 10l4.553-2.069A1 1 0 0121 8.82v6.361a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="font-bold text-gray-800">Session Presentations</h3>
          </div>
          <p class="text-sm text-gray-600 leading-relaxed">
            Oral presentations of contributed abstracts are usually <strong>10 minutes</strong> for presentation and
            <strong>5 minutes</strong> for questions.
          </p>
        </section>

        <!-- ePoster Sessions -->
        <section class="bg-white rounded-2xl shadow-sm p-7">
          <div class="flex items-center gap-3 mb-4">
            <div class="h-9 w-9 rounded-xl flex items-center justify-center flex-shrink-0" style="background-color: #F7941D;">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="font-bold text-gray-800">ePoster Sessions</h3>
          </div>
          <ul class="space-y-2">
            <li class="flex items-start gap-2 text-sm text-gray-600 leading-relaxed">
              <span class="mt-1.5 h-1.5 w-1.5 rounded-full flex-shrink-0" style="background-color: #F7941D;"></span>
              Authors must ensure the title and content of their posters correspond to the abstract printed in the program book.
            </li>
            <li class="flex items-start gap-2 text-sm text-gray-600 leading-relaxed">
              <span class="mt-1.5 h-1.5 w-1.5 rounded-full flex-shrink-0" style="background-color: #F7941D;"></span>
              ePoster will be designed in a PowerPoint format.
            </li>
            <li class="flex items-start gap-2 text-sm text-gray-600 leading-relaxed">
              <span class="mt-1.5 h-1.5 w-1.5 rounded-full flex-shrink-0" style="background-color: #F7941D;"></span>
              A template will be provided upon confirmation of your abstract for ePoster designing.
            </li>
          </ul>
        </section>
      </div>

      <!-- ─ Withdrawing ──────────────────────────────────────────────────────── -->
      <section class="bg-amber-50 border border-amber-200 rounded-2xl p-7">
        <div class="flex items-start gap-3">
          <svg class="w-6 h-6 text-amber-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div>
            <h3 class="font-bold text-amber-800 mb-1">Withdrawing an Abstract</h3>
            <p class="text-sm text-amber-700 leading-relaxed">
              Only the first author or submitter may withdraw an abstract from the program. Requests for withdrawals must
              come to the ECSA-HC 2026 in writing, by email to
              <a href="mailto:abstracts2019@ecsahc.org" class="font-semibold underline hover:opacity-80">abstracts2019@ecsahc.org</a>.
            </p>
          </div>
        </div>
      </section>

      <!-- ─ Submit Abstract Form ──────────────────────────────────────────────── -->
      <section class="bg-white rounded-2xl shadow-sm p-8" id="submit">
        <div class="flex items-center gap-3 mb-6">
          <div class="h-10 w-10 rounded-xl flex items-center justify-center flex-shrink-0" style="background-color: #0095B6;">
            <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
          </div>
          <div>
            <h2 class="text-2xl font-bold text-gray-800">Submit Your Abstract</h2>
            <p class="text-sm text-gray-500 mt-0.5">Fill in the form below to submit your abstract for ECSA-HC 2026.</p>
          </div>
        </div>

        <form @submit.prevent="submitAbstract" class="space-y-5">
          <div class="grid gap-4 sm:grid-cols-2">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">First Name <span class="text-red-500">*</span></label>
              <input v-model="form.first_name" type="text" required placeholder="Jane"
                class="w-full px-4 py-2.5 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#0095B6]" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Last Name <span class="text-red-500">*</span></label>
              <input v-model="form.last_name" type="text" required placeholder="Doe"
                class="w-full px-4 py-2.5 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#0095B6]" />
            </div>
          </div>

          <div class="grid gap-4 sm:grid-cols-2">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email Address <span class="text-red-500">*</span></label>
              <input v-model="form.email" type="email" required placeholder="jane@example.org"
                class="w-full px-4 py-2.5 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#0095B6]" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Institution / Organisation <span class="text-red-500">*</span></label>
              <input v-model="form.institution" type="text" required placeholder="Ministry of Health, Tanzania"
                class="w-full px-4 py-2.5 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#0095B6]" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Abstract Title <span class="text-red-500">*</span></label>
            <input v-model="form.title" type="text" required placeholder="Title of your abstract"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#0095B6]" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Scientific Track <span class="text-red-500">*</span></label>
            <select v-model="form.track" required
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#0095B6]">
              <option disabled value="">Select a track</option>
              <template v-for="group in scientificTracks" :key="group.number">
                <optgroup :label="`${group.number}. ${group.title}`">
                  <option v-for="sub in group.subtracks" :key="sub.code" :value="sub.code">
                    {{ sub.code }}: {{ sub.label }}
                  </option>
                </optgroup>
              </template>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Abstract Body <span class="text-red-500">*</span>
              <span class="ml-2 text-xs font-normal text-gray-400">(max 300 words)</span>
            </label>
            <textarea v-model="form.body" rows="7" required
              placeholder="Write or paste your abstract here (maximum 300 words)..."
              class="w-full px-4 py-2.5 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#0095B6]"></textarea>
            <p class="text-xs text-gray-400 mt-1 text-right">{{ wordCount }} / 300 words</p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Presentation Preference</label>
            <div class="flex gap-4 flex-wrap">
              <label class="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
                <input type="radio" v-model="form.preference" value="oral" class="accent-[#0095B6]" />
                Oral Presentation
              </label>
              <label class="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
                <input type="radio" v-model="form.preference" value="poster" class="accent-[#0095B6]" />
                ePoster Session
              </label>
              <label class="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
                <input type="radio" v-model="form.preference" value="either" class="accent-[#0095B6]" />
                Either
              </label>
            </div>
          </div>

          <!-- File upload -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Upload Abstract Document <span class="text-gray-400">(optional)</span></label>
            <div
              class="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-[#0095B6] hover:bg-blue-50/20 transition cursor-pointer"
              @click="triggerFileInput"
              @dragover.prevent
              @drop.prevent="handleDrop"
            >
              <input ref="fileInput" type="file" accept=".pdf,.doc,.docx" class="hidden" @change="handleFileChange" />
              <svg class="mx-auto h-10 w-10 text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                  d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <p class="text-sm text-gray-500">
                <span class="font-semibold" style="color: #0095B6;">Click to upload</span> or drag and drop
              </p>
              <p class="text-xs text-gray-400 mt-1">PDF, DOC or DOCX — max 10 MB</p>
              <p v-if="selectedFile" class="mt-3 text-sm font-medium text-gray-700">
                Selected: {{ selectedFile.name }}
              </p>
            </div>
          </div>

          <!-- Success / error feedback -->
          <div v-if="submitted" class="flex items-center gap-3 text-green-700 bg-green-50 border border-green-200 rounded-xl px-5 py-4 text-sm">
            <svg class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <div>
              <p class="font-semibold">Abstract submitted successfully!</p>
              <p class="text-green-600 mt-0.5">You will receive a confirmation email at <strong>{{ form.email }}</strong>. Notification of acceptance will be sent before 5th July 2026.</p>
            </div>
          </div>

          <div class="flex items-center gap-4 flex-wrap">
            <button
              type="submit"
              :disabled="submitting"
              class="px-8 py-3 rounded-full font-semibold text-white text-sm transition hover:opacity-90 disabled:opacity-60 shadow-sm"
              style="background-color: #0095B6;"
            >
              {{ submitting ? 'Submitting…' : 'Submit Abstract →' }}
            </button>
            <p class="text-xs text-gray-400">
              For technical support contact
              <a href="mailto:abstracts2019@ecsahc.org" class="underline" style="color: #0095B6;">abstracts2019@ecsahc.org</a>
            </p>
          </div>
        </form>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const callForAbstractItems = [
  'Abstracts can only be submitted online via our website (abstract submission); submissions by email or any other means will not be considered.',
  'All abstracts must be written in English.',
  "It is the author's responsibility to submit a correct abstract. Any errors in spelling, grammar or scientific fact in the abstract text will be reproduced as typed by the author. Abstract titles will be subject to a spell check if the abstract is selected for presentation.",
]

const scientificTracks = [
  {
    number: '1',
    title: 'Regional Health Security & Pandemic Agreement Implementation',
    lead: 'Mohamed',
    color: '#0095B6',
    subtracks: [
      { code: 'Track 1.1', label: 'Operationalizing the Pandemic Agreement and IHR (2005) Reforms in ECSA region' },
      { code: 'Track 1.2', label: 'Surveillance, Early Warning, and One Health Intelligence for preparedness and response' },
      { code: 'Track 1.3', label: 'Prevention and Control of Antimicrobial Resistance' },
      { code: 'Track 1.4', label: 'Workforce Capacity and Emergency Preparedness' },
    ],
  },
  {
    number: '2',
    title: 'Digital Innovation for Resilient Health Systems (including AI)',
    lead: 'Timothy',
    color: '#F7941D',
    subtracks: [
      { code: 'Track 2.1', label: 'Scaling Digital Health Solutions for Service Delivery and UHC' },
      { code: 'Track 2.2', label: 'Artificial Intelligence and Data-Driven Decision-Making in Health Systems' },
    ],
  },
  {
    number: '3',
    title: 'Harnessing Demographic Dividend & Youth Engagement',
    lead: 'Andrew',
    color: '#007A96',
    subtracks: [
      { code: 'Track 3.1', label: 'Youth-Centered Health Systems and Meaningful Engagement' },
      { code: 'Track 3.2', label: 'Leveraging the Demographic Dividend for Health and Economic Development' },
      { code: 'Track 3.3', label: 'Investing in Adolescent and Youth Sexual and Reproductive Health' },
      { code: 'Track 3.4', label: 'Digital Innovation and Youth-Led Solutions in Health' },
      { code: 'Track 3.5', label: 'Engaging Young Professionals in Leadership, Research, and Policy Development' },
      { code: 'Track 3.6', label: 'Strengthening Adolescent Nutrition with Evidence-Based Interventions to Promote Healthy Youth Development' },
    ],
  },
  {
    number: '4',
    title: 'Global Health Diplomacy Amid Reforms',
    lead: 'Sibbusiso',
    color: '#c0392b',
    subtracks: [
      { code: 'Track 4.1', label: 'Advancing Regional Voice and Negotiation Power in Global Health Governance' },
      { code: 'Track 4.2', label: 'Strategic Positioning of ECSA-HC Priorities in Global Health Agendas' },
    ],
  },
  {
    number: '5',
    title: 'Sustainable Financing & Partnerships',
    lead: 'Edward',
    color: '#27ae60',
    subtracks: [
      { code: 'Track 5.1', label: 'Domestic Resource Mobilization and Innovative Health Financing Models' },
      { code: 'Track 5.2', label: 'Transforming Partnerships for Sustainable and Resilient Health Systems' },
    ],
  },
  {
    number: '6',
    title: 'Innovation, Health Research & Development in ECSA',
    lead: 'Sebentile',
    color: '#8e44ad',
    subtracks: [
      { code: 'Track 6.1', label: 'Innovations in RMNCAH and Priority Population Health Interventions' },
      { code: 'Track 6.2', label: 'Advancing Health Research, Innovation Ecosystems and Knowledge Translation' },
    ],
  },
  {
    number: '7',
    title: 'Quality of Care & Patient Safety',
    lead: 'Tina',
    color: '#e67e22',
    subtracks: [
      { code: 'Track 7.1', label: 'Improving Quality of Care Across the Continuum of Services' },
      { code: 'Track 7.2', label: 'Patient Safety Systems and Culture in Health Care' },
    ],
  },
]

const submittingItems = [
  'Abstracts do not comply with style guidelines, including excessive length (contributed abstract body text is limited to approximately 300 words)',
  'Abstracts contain inappropriate content, e.g. graph, pictures, etc.',
  'Abstracts fall outside of the topical scope of the meeting',
]

const form = ref({
  first_name: '',
  last_name: '',
  email: '',
  institution: '',
  title: '',
  track: '',
  body: '',
  preference: 'either',
})

const fileInput = ref(null)
const selectedFile = ref(null)
const submitting = ref(false)
const submitted = ref(false)

const wordCount = computed(() => {
  const text = form.value.body.trim()
  return text ? text.split(/\s+/).length : 0
})

const triggerFileInput = () => fileInput.value?.click()

const handleFileChange = (e) => {
  selectedFile.value = e.target.files[0] || null
}

const handleDrop = (e) => {
  selectedFile.value = e.dataTransfer.files[0] || null
}

const submitAbstract = async () => {
  submitting.value = true
  // Dummy submission — replace with real API call when endpoint is available
  await new Promise(resolve => setTimeout(resolve, 1400))
  submitted.value = true
  submitting.value = false
}
</script>
