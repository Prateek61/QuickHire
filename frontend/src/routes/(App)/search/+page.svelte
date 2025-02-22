<script lang="ts">
  let search = "";
  let sortBy = "Most Relevant";
  let professionals = [
    { name: "Britney Spears", role: "Singer", rate: "$65/hr", rating: "4.5 Stars", tags: ["Pop", "Acting"], description: "Specialized in pop songs. 8+ years of experience." },
    { name: "Cave Johnson", role: "Scientist", rate: "$85/hr", rating: "5 Stars", tags: ["AI", "Robotics"], description: "Founder at Aperture Labs. Creator @GLaDOS" }
  ];
</script>
  
<div class="flex flex-col min-h-screen bg-gradient-to-r from-blue-50 to-purple-100 p-4 text-gray-900">
  <!-- Main Content -->
  <main class="flex-1 ml-0 md:ml-6">
    <div class="flex flex-col md:flex-row justify-between mb-4 px-7 pb-5">
      <div class="relative w-full md:w-1/2 flex mb-4 md:mb-0">
        <input type="text" bind:value={search} placeholder="Search skills, professionals..." class="border p-3 w-full bg-white rounded-md shadow-sm" />
        <button class="ml-2 p-3 bg-blue-500 text-white rounded-md shadow-sm flex items-center cursor-pointer hover:bg-blue-600">
          <svg class="text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 22" stroke="currentColor" width="20" height="20">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-4.35-4.35m1.35-5.65a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </button>
      </div>
      <select bind:value={sortBy} class="border p-2 bg-white rounded-md shadow-sm w-full md:w-1/4">
        <option>Most Relevant</option>
        <option>Highest Rated</option>
        <option>Lowest Price</option>
      </select>
    </div>
  
    <div class="bg-white p-6 shadow-lg rounded-xl text-gray-900 w-full md:w-3/4 mx-auto">
      {#each professionals as prof}
        <div class="border-b py-6 flex flex-col md:flex-row items-start md:items-center space-y-4 md:space-y-0 md:space-x-4">
          <div class="w-16 h-16 bg-gray-300 rounded-full flex items-center justify-center text-lg font-bold text-gray-700">{prof.name[0]}</div>
          <div>
            <h3 class="font-bold text-lg">{prof.name}</h3>
            <p class="text-gray-700">{prof.role} - <span class="text-blue-500">{prof.rate}</span> - ⭐ {prof.rating}</p>
            <p class="text-sm text-gray-600">{prof.description}</p>
            <div class="mt-2 flex flex-wrap space-x-2">
              {#each prof.tags as tag}
                <span class="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-xs font-medium">{tag}</span>
              {/each}
            </div>
            <button class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">View Profile</button>
          </div>
        </div>
      {/each}
    </div>
  
    <!-- Pagination -->
    <div class="mt-6 flex justify-center space-x-2">
      <button class="px-4 py-2 border rounded-lg bg-gray-200 text-gray-800 hover:bg-gray-300">Previous</button>
      <button class="px-4 py-2 bg-blue-500 text-white rounded-lg">1</button>
      <button class="px-4 py-2 border rounded-lg bg-gray-200 text-gray-800 hover:bg-gray-300">2</button>
      <button class="px-4 py-2 border rounded-lg bg-gray-200 text-gray-800 hover:bg-gray-300">3</button>
      <button class="px-4 py-2 border rounded-lg bg-gray-200 text-gray-800 hover:bg-gray-300">Next</button>
    </div>
  </main>
</div>
