  <script>
    import LoginForm from './Login.svelte';
    import penguin from '$lib/images/penguin.png';
  </script>
  
  <section class="bg-slate-50 flex justify-between items-center min-h-[90vh] font-cambria " >
    
    <div class="flex-1 flex-col justify-center items-center max-w-[80%] h-[90vh]">
        <img  class = "mx-[auto] mt-[135px] mb-[20px] w-[120px]" src="{penguin}" alt="QuickHire Logo">
        <h1 class="text-center text-[3.5rem] text-[#f5a60a] mb-[20px]" >Welcome to QuickHire</h1>
        <p class="text-[1.5rem] text-[#0840a7] italic mb-[20px] mt-[20px] ml-[250px]" >-A platform to find Professionals</p>
    </div>
    <LoginForm class="flex-1"/>

  </section>