<template>
  <footer class="bg-gray-800 text-white py-4">
    <div class="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
      <!-- Left Side: Copyright + Privacy Policy -->
      <div class="flex flex-col sm:flex-row items-center gap-4 sm:gap-6 text-sm text-center sm:text-left">
        <span>&copy; 2025 <span class="font-semibold">ECSA-HC</span>. All rights reserved.</span>
        <a href="/privacy-policy" class="hover:underline">
          Privacy Policy
        </a>
      </div>

      <!-- Right Side: Social Icons -->
      <div class="flex items-center gap-5">
        <a href="#" class="hover:text-bondi-blue" aria-label="LinkedIn">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M4.98 3.5C3.88 3.5 3 4.38 3 5.48s.88 1.98 1.98 1.98A1.98 1.98 0 007.96 5.5C7.96 4.38 7.08 3.5 5.98 3.5zM3.5 8.25h3V20.5h-3V8.25zM9.5 8.25h2.87v1.69h.04c.4-.76 1.37-1.56 2.83-1.56 3.03 0 3.59 1.99 3.59 4.57v7.55h-3v-6.7c0-1.6-.03-3.66-2.23-3.66-2.24 0-2.59 1.74-2.59 3.54v6.82h-3V8.25z"/>
          </svg>
        </a>

        <a href="#" class="hover:text-bondi-blue" aria-label="X (Twitter)">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M22.46 6c-.77.35-1.6.58-2.46.69a4.26 4.26 0 001.88-2.34 8.56 8.56 0 01-2.7 1.03 4.23 4.23 0 00-7.21 3.86A12 12 0 013 5.15a4.22 4.22 0 001.31 5.64 4.2 4.2 0 01-1.91-.53v.05a4.24 4.24 0 003.39 4.14 4.24 4.24 0 01-1.9.07 4.25 4.25 0 003.96 2.95 8.5 8.5 0 01-5.29 1.83A8.63 8.63 0 012 19.54a12 12 0 006.29 1.84c7.55 0 11.68-6.26 11.68-11.68 0-.18-.01-.35-.02-.53A8.3 8.3 0 0022.46 6z"/>
          </svg>
        </a>

        <a href="#" class="hover:text-bondi-blue" aria-label="Facebook">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M22 12a10 10 0 10-11.63 9.87v-6.99h-2.4v-2.88h2.4V9.41c0-2.37 1.41-3.68 3.57-3.68 1.03 0 2.11.18 2.11.18v2.31h-1.19c-1.17 0-1.54.73-1.54 1.48v1.77h2.63l-.42 2.88h-2.21v6.99A10 10 0 0022 12z"/>
          </svg>
        </a>

        <a href="#" class="hover:text-bondi-blue" aria-label="Instagram">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M7 2C4.243 2 2 4.243 2 7v10c0 2.757 2.243 5 5 5h10c2.757 0 5-2.243 5-5V7c0-2.757-2.243-5-5-5H7zm8.25 3.5a1.25 1.25 0 110 2.5 1.25 1.25 0 010-2.5zM12 7a5 5 0 110 10 5 5 0 010-10zm0 2a3 3 0 100 6 3 3 0 000-6z"/>
          </svg>
        </a>
      </div>
    </div>
  </footer>
</template>

<script setup>
// No script needed for static footer
</script>
