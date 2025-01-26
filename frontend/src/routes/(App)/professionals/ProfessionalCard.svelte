<!-- Card representing the details of a single professional -->
 <!-- A profesional has quantities: name, skill, hourlyrate, experience  -->

<script>
    export let professional;
</script>

<div class="bg-surface-800 p-4 rounded-lg shadow-md w-full max-w-md">
    <h1 class="text-2xl font-bold text-center text-surface-50 mb-6">{professional.name}</h1>

    <div class="flex items-center space-x-2">
        <span class="text-primary-400">Skill:</span>
        <span class="text-surface-50">{professional.skill}</span>
    </div>

    <div class="flex items-center space-x-2">
        <span class="text-primary-400">Hourly Rate:</span>
        <span class="text-surface-50">{professional.hourly_rate}</span>
    </div>

    <div class="flex items-center space-x-2">
        <span class="text-primary-400">Experience:</span>
        <span class="text-surface-50">{professional.experience}</span>
    </div>

    <button class="w-full bg-primary-700 text-surface-50 py-2 rounded-md font-semibold hover:bg-primary-800 transition-colors duration-200 mt-4">
        Hire {professional.name}
    </button>

</div>
