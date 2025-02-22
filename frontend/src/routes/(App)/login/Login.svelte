<script lang="ts">
    let email = '';
    let password = '';
</script>
  
  <div class = "text-black flex justify-center items-center bg-[#4c7b8b] h-[90vh] w-[50vw] ">
    <div class="bg-[#ffffff] p-[20px] rounded-[12px] shadow-md w-[60%] h-[70%] ">
        <h2 class="mb-[17px] text-[1.5rem] text-center">Login</h2>
        <form>
            <div class="mb-[13px]">
                <label class="block mb-[5px] text-[1rem] text-[#333] " for="email">Email</label>
                <input class="w-full p-[10px] border border-[#ccc] rounded-[8px] text-[1.1rem] focus:border-[#007bff] focus:outline-none focus:shadow-[0_0_4px_rgba(0,123,255,0.5)]" type="email" id="email" name="email" placeholder="Enter your email" required>
            </div>

            <div class="mb-[13px]">
                <label class="block mb-[5px] text-[1rem] text-[#333] " for="password">Password</label>
                <input class="w-full p-[10px] border border-[#ccc] rounded-[8px] text-[1.1rem] focus:border-[#007bff] focus:outline-none focus:shadow-[0_0_4px_rgba(0,123,255,0.5)]" 
                type="password" id="password" name="password" placeholder="Enter your password" required>
            </div>
            
            <button type="submit" class="w-full p-[10px] bg-[#007bff] text-white border-none rounded-[8px] text-[1rem] cursor-pointer transition-colors duration-300 hover:bg-[#0056b3] mb-[10px]">Login as Client</button>
            <button type="button" class="w-full p-[10px] bg-[#28a745] text-white border-none rounded-[8px] text-[1rem] cursor-pointer transition-colors duration-300 hover:bg-[#218838]" on:click={() => window.location.href = '../Dashboard'}>Login as Professional</button>
        </form>
        <p class="mt-[15px] text-center text-[1rem]">Don't have an account? <a class="text-[#007bff] no-underline hover:underline" href="../signup">Sign up</a></p>
    </div>
  </div>