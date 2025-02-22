<script>
    let profile = {
      name: "John Doe",
      title: "Carpenter",
      location: "Kathmandu valley, Nepal",
      about: "I am a professional carpenter and specialized in custom furniture and home decor. I am also skilled in woodwork and carpentry. I have worked on various projects and have a good reputation in the industry. I am passionate about my work and always deliver high-quality results.",
      skills: ["Woodwork", "Furniture Design", "Home Decor", "Carpentry"],
      experience:  "10 years of experience in carpentry and woodwork",
      contact: {
        phone: "+1 234 567 890",
        email: "johndoe@email.com"
      },
      hourlyRate: "NRS 50/hr",
      rating: 5.0,
      reviews: [
        {
          client: "Jane Smith",
          feedback: "John did an amazing job with our custom furniture. Highly recommend!",
          rating: 5
        },
        {
          client: "Mike Johnson",
          feedback: "Professional and skilled carpenter. Delivered high-quality work on time.",
          rating: 4.5
        },
        {
          client: "Emily Davis",
          feedback: "Great attention to detail and very reliable. Will hire again.",
          rating: 5
        }
      ]
    };
</script>

<main class="bg-gray-400">
    <div class="max-w-4xl mx-auto p-6 space-y-6 text-gray-900">
        <div class="p-6 flex flex-col lg:flex-row items-center space-y-6 lg:space-y-0 lg:space-x-6 shadow-lg rounded-2xl bg-white border border-gray-200">
            <div class="w-24 h-24 rounded-full border-4 border-gray-300 bg-gray-100 overflow-hidden">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTA78Na63ws7B7EAWYgTr9BxhX_Z8oLa1nvOA&s" alt="" class="w-full h-full object-cover" /></div>
            <div class="flex-1">
            <h2 class="text-2xl font-semibold text-gray-900">{profile.name}</h2>
            <p class="text-gray-600">{profile.title}</p>
            <p class="text-gray-500 flex items-center"><span class="w-4 h-4 mr-2">📍</span> {profile.location}</p>
            </div>
            <button class="mt-4 lg:mt-0 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">Hire me</button>
        </div>

        <div class="p-6 shadow-lg rounded-2xl bg-white border border-gray-200">
            <h3 class="text-xl font-semibold mb-4">About Me</h3>
            <p class="text-gray-700">{profile.about}</p>
        </div>

        <div class="p-6 shadow-lg rounded-2xl bg-white border border-gray-200">
            <h3 class="text-xl font-semibold mb-4">Skills</h3>
            <div class="flex flex-wrap gap-2">
                {#each profile.skills as skill}
                <span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">{skill}</span>
                {/each}
            </div>
        </div>

        <div class="p-6 shadow-lg rounded-2xl bg-white border border-gray-200">
            <h3 class="text-xl font-semibold mb-4">Experience</h3>
            <p class="text-gray-700">{profile.experience}</p>
        </div>

        <div class="p-6 shadow-lg rounded-2xl bg-white border border-gray-200">
            <h3 class="text-xl font-semibold mb-4">Contact</h3>
            <p class="text-gray-700 flex items-center"><span class="w-4 h-4 mr-2">📞</span> {profile.contact.phone}</p>
            <p class="text-gray-700 flex items-center"><span class="w-4 h-4 mr-2">📧</span> {profile.contact.email}</p>
        </div>

        <div class="p-6 shadow-lg rounded-2xl bg-white border border-gray-200">
            <h3 class="text-xl font-semibold mb-4">Hourly Rate</h3>
            <p class="text-gray-900 text-lg font-bold">{profile.hourlyRate}</p>
        </div>

        <div class="p-6 shadow-lg rounded-2xl bg-white border border-gray-200">
            <h3 class="text-xl font-semibold mb-4">Reviews & Ratings</h3>
            <div class="flex items-center text-yellow-500">
                {#each Array(5) as _, i}
                <span class="w-5 h-5">⭐</span>
                {/each}
                <span class="text-gray-700 ml-2">{profile.rating} ({profile.reviews.length} Reviews)</span>
            </div>
            {#each profile.reviews as review}
            <div class="mt-4 p-4 bg-gray-100 rounded-lg">
                <p class="text-gray-900 font-semibold">{review.client}</p>
                <p class="text-gray-700">{review.feedback}</p>
                <div class="flex items-center text-yellow-500">
                    {#each Array(Math.round(review.rating)) as _, i}
                    <span class="w-4 h-4">⭐</span>
                    {/each}
                </div>
            </div>
            {/each}
        </div>
    </div>
</main>