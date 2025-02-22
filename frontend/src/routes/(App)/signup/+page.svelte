<script>
    let isClientForm = true;
    let fullName = "";
    let email = "";
    let phone = "";
    let password = "";
    let confirmPassword = "";
    let hourlyRate = "";
    let availability = "";
    let experience = "";
    let location = "";
    let coverLetter = "";
    let selectedSkills = [];
    let skills = ["Carpeting", "Mechanic", "Chef", "Plumbing", "Web Development"];

    function handleSignup() {
        alert(`Signing up ${fullName}`);
    }
</script>

<div class="min-h-screen bg-cover bg-center" style="background-image: url('https://images.unsplash.com/photo-1472289065668-ce650ac443d2?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGxvZ2lufGVufDB8fDB8fHww');">
    <div class="py-[50px] flex items-center justify-center min-h-screen px-4 bg-black bg-opacity-50">
        <div class="w-full max-w-[600px] bg-white p-7 rounded-2xl shadow-xl border border-gray-200">
            <h2 class="text-3xl font-bold text-center text-black mb-6">{isClientForm ? 'Client Signup' : 'Professional Signup'}</h2>
            <button class="w-full bg-[#4C7B8B] text-black font-bold py-2 rounded-md mb-4" on:click={() => isClientForm = !isClientForm}>
                Switch to {isClientForm ? 'Professional' : 'Client'} Signup
            </button>

            <form on:submit|preventDefault={handleSignup} class="space-y-4">
                <!-- Full Name -->
                <div>
                    <label class="block text-black font-medium">Full Name</label>
                    <input type="text" bind:value={fullName} placeholder="Enter your full name" class="w-full text-black p-3 border rounded-md focus:border-[#007bff] focus:outline-none focus:shadow-[0_0_4px_rgba(0,123,255,0.5)]" required />
                </div>

                <!-- Email -->
                <div>
                    <label class="block text-black font-medium">Email</label>
                    <input type="email" bind:value={email} placeholder="Enter your email" class="w-full text-black p-3 border rounded-md focus:border-[#007bff] focus:outline-none focus:shadow-[0_0_4px_rgba(0,123,255,0.5)]" required />
                </div>

                <!-- Phone Number -->
                <div>
                    <label class="block text-black font-medium">Phone No</label>
                    <input type="tel" bind:value={phone} placeholder="Enter your phone number" class="w-full text-black p-3 border rounded-md focus:border-[#007bff] focus:outline-none focus:shadow-[0_0_4px_rgba(0,123,255,0.5)]" required />
                </div>

                <!-- Password -->
                <div>
                    <label class="block text-black font-medium">Password</label>
                    <input type="password" bind:value={password} placeholder="At least 8 characters" class="w-full text-black p-3 border rounded-md focus:border-[#007bff] focus:outline-none focus:shadow-[0_0_4px_rgba(0,123,255,0.5)]" required minlength="8" />
                </div>

                <!-- Confirm Password -->
                <div>
                    <label class="block text-black font-medium">Confirm Password</label>
                    <input type="password" bind:value={confirmPassword} placeholder="Re-enter password" class="w-full text-black p-3 border rounded-md focus:border-[#007bff] focus:outline-none focus:shadow-[0_0_4px_rgba(0,123,255,0.5)]" required minlength="8" />
                </div>

                {#if !isClientForm}
                <!-- Professional Specific Fields -->
                <div>
                    <label class="block text-black font-medium">Hourly Rate</label>
                    <input type="text" bind:value={hourlyRate} placeholder="Enter your hourly rate" class="w-full text-black p-3 border rounded-md focus:border-[#007bff] focus:outline-none focus:shadow-[0_0_4px_rgba(0,123,255,0.5)]" />
                </div>

                <div>
                    <label class="block text-black font-medium">Availability</label>
                    <input type="text" bind:value={availability} placeholder="e.g., Full-time, Part-time" class="w-full text-black p-3 border rounded-md focus:border-[#007bff] focus:outline-none focus:shadow-[0_0_4px_rgba(0,123,255,0.5)]" />
                </div>

                <div>
                    <label class="block text-black font-medium">Experience (Years)</label>
                    <input type="text" bind:value={experience} placeholder="Years of experience" class="w-full text-black p-3 border rounded-md focus:border-[#007bff] focus:outline-none focus:shadow-[0_0_4px_rgba(0,123,255,0.5)]" />
                </div>

                <div>
                    <label class="block text-black font-medium">Location</label>
                    <input type="text" bind:value={location} placeholder="City, State" class="w-full text-black p-3 border rounded-md focus:border-[#007bff] focus:outline-none focus:shadow-[0_0_4px_rgba(0,123,255,0.5)]" />
                </div>

                <div>
                    <label class="block text-black font-medium">Cover Letter</label>
                    <textarea bind:value={coverLetter} placeholder="Briefly introduce yourself" class="w-full text-black p-3 border rounded-md focus:border-[#007bff] focus:outline-none focus:shadow-[0_0_4px_rgba(0,123,255,0.5)]"></textarea>
                </div>

                <div>
                    <label class="block text-black font-medium">Select Skills</label>
                    <div class="flex flex-wrap gap-2">
                        {#each skills as skill}
                            <button type="button" class="bg-gray-600 px-4 py-2 rounded-md" on:click={() => {
                                if (selectedSkills.includes(skill)) {
                                    selectedSkills = selectedSkills.filter(s => s !== skill);
                                } else {
                                    selectedSkills = [...selectedSkills, skill];
                                }
                            }}>
                                {skill}
                            </button>
                        {/each}
                    </div>
                </div>
                {/if}

                <!-- Sign-Up Button -->
                <button type="submit" class="w-full bg-blue-900 text-white text-lg font-bold py-3 rounded-md hover:bg-blue-700 transition duration-200">
                    Sign Up
                </button>
            </form>
        </div>
    </div>
</div>
