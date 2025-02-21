<script>
    let fullName = "";
    let email = "";
    let phone = "";
    let password = "";
    let confirmPassword = "";

    function handleSignup() {
        alert(`Signing up ${fullName}`);
    }
</script>

<div class="min-h-screen bg-cover bg-center" style="background-image: url('https://images.unsplash.com/photo-1472289065668-ce650ac443d2?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGxvZ2lufGVufDB8fDB8fHww');">

	<div class="py-[50px] flex items-center justify-center min-h-screen px-4 bg-black bg-opacity-50">
		<div class="w-full max-w-md bg-[23486A] p-6 rounded-2xl shadow-xl border border-gray-200">
			<h2 class="text-3xl font-bold text-center text-white mb-6">Sign Up</h2>

			<form on:submit|preventDefault={handleSignup} class="space-y-4">
				<!-- Full Name -->
				<div>
					<label for="fullName" class="block text-white font-medium">Full Name</label>
					<input id="fullName" type="text" bind:value={fullName} placeholder="Enter your full name"
						class="w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required />
				</div>

				<!-- Email -->
				<div>
					<label for="email" class="block text-white font-medium">Email</label>
					<input id="email" type="email" bind:value={email} placeholder="Enter your email"
						class="w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required />
					<p class="text-sm text-gray-300">We'll never share your email with anyone else.</p>
				</div>

				<!-- Phone Number -->
				<div>
					<label for="phone" class="block text-white font-medium">Phone No</label>
					<input id="phone" type="tel" bind:value={phone} placeholder="Enter your phone number"
						class="w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required />
				</div>

				<!-- Password -->
				<div>
					<label for="password" class="block text-white font-medium">Password</label>
					<input id="password" type="password" bind:value={password} placeholder="Password must be at least 8 characters long"
						class="w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required minlength="8" />
				</div>

				<!-- Confirm Password -->
				<div>
					<label for="confirmPassword" class="block text-white font-medium">Confirm Password</label>
					<input id="confirmPassword" type="password" bind:value={confirmPassword} placeholder="Password must be at least 8 characters long"
						class="w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required minlength="8" />
				</div>

				<!-- Sign-Up Button -->
				<button type="submit"
					class="w-full bg-blue-600 text-white font-bold py-3 rounded-md hover:bg-blue-700 transition duration-200">
					Sign Up
				</button>
			</form>
		</div>
	</div>
</div>
