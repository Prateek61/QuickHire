<script context="module">
    export const load = async ({ fetch }) => {
        const response = await fetch('/api/professionals');
        const professionals = await response.json();
        return { props: { professionals } };
    };
</script>

<script>
    import ProfessionalCard from "./ProfessionalCard.svelte";

    export let data;
    // export let error;

    let professionals = [];

    if (data.props.ok) {
        professionals = data.props.professionals;

        // Maybe console.log to see the professionals
    } else {
        // TODO: Handle error
        console.log(data.props.error);
    }
</script>

<div class="min-h-screen bg-surface-900 text-surface-50 py-8">
	<div class="container mx-auto px-4">
		<h1 class="text-3xl font-bold mb-6">Browse Professionals</h1>
		
		<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
			<!-- {#each professionals as professional}
				<ProfessionalCard {professional} />
			{/each} -->
		</div>
	</div>
</div>


