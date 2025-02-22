<script>
	import penguin from '$lib/images/penguin.png';
</script>

<div class=" bg-gradient-to-br from-blue-50 to-indigo-50">
	<div class="flex items-center justify-center min-h-[90vh] py-12 px-4 sm:px-6 lg:px-8">
		<div
			class="flex flex-col md:flex-row w-full max-w-6xl bg-white rounded-2xl shadow-2xl overflow-hidden transform hover:scale-[1.02] transition-transform duration-300"
		>
			<!-- Left Section -->
			<div
				class="w-full md:w-1/2 p-8 md:p-12 bg-gradient-to-br from-indigo-500 to-blue-600 text-white"
			>
				<div class="flex flex-col h-full justify-center">
					<div class="bg-white/10 p-6 rounded-2xl backdrop-blur-sm">
						<img
							class="mx-auto w-32 h-32 object-contain filter drop-shadow-lg transform hover:rotate-6 transition-transform duration-300"
							src={penguin}
							alt="QuickHire Logo"
						/>
						<h1 class="text-4xl font-bold mt-8 mb-4">About QuickHire</h1>
						<p class="text-xl italic text-blue-100">
							"Connecting Professionals with Opportunities."
						</p>
					</div>

					<div class="mt-8 space-y-4">
						<div class="flex items-center space-x-3">
							<div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
								<svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
									<path
										d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"
									/>
								</svg>
							</div>
							<span class="text-sm">Join our growing community</span>
						</div>
						<div class="flex items-center space-x-3">
							<div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
								<svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
									<path
										d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"
									/>
								</svg>
							</div>
							<span class="text-sm">Connect with top talent</span>
						</div>
					</div>
				</div>
			</div>

			<!-- Right Section -->
			<div class="w-full md:w-1/2 p-8 md:p-12 bg-white">
				<div class="h-full flex flex-col justify-center">
					<div class="mb-8">
						<h2 class="text-3xl font-bold text-gray-800 mb-4">Our Mission</h2>
						<p class="text-gray-600 leading-relaxed">
							QuickHire is a platform dedicated to bridging the gap between professionals and
							clients. Whether you're a freelancer, a business, or a company looking for skilled
							individuals, we make the process seamless and efficient.
						</p>
					</div>

					<div>
						<h2 class="text-3xl font-bold text-gray-800 mb-6">Why Choose Us?</h2>
						<div class="space-y-4">
							<div class="flex items-center space-x-4 p-4 bg-blue-50 rounded-lg">
								<div
									class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white"
								>
									<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M13 10V3L4 14h7v7l9-11h-7z"
										/>
									</svg>
								</div>
								<span class="text-gray-700">Fast and reliable hiring process</span>
							</div>
							<div class="flex items-center space-x-4 p-4 bg-blue-50 rounded-lg">
								<div
									class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white"
								>
									<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
										/>
									</svg>
								</div>
								<span class="text-gray-700">Verified professionals</span>
							</div>
							<div class="flex items-center space-x-4 p-4 bg-blue-50 rounded-lg">
								<div
									class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white"
								>
									<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
										/>
									</svg>
								</div>
								<span class="text-gray-700">Secure payment and communication</span>
							</div>
							<div class="flex items-center space-x-4 p-4 bg-blue-50 rounded-lg">
								<div
									class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white"
								>
									<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
										/>
									</svg>
								</div>
								<span class="text-gray-700">24/7 customer support</span>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
