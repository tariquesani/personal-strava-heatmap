% rebase('layout.tpl', title='Athlete')

<main class="container mt-4 pt-3 d-flex justify-content-center">
    <div class="col-md-8">
        <div class="card">
            <div class="card-body">
                <h2 class="card-title text-center mb-4">Athlete fetched from Strava</h2>
                <div class="row">
                    <div class="col-md-4 text-center">
                        <img src="{{ athlete['profile'] }}" alt="Profile Image" class="img-fluid rounded-circle mb-3">
                    </div>
                    <div class="col-md-8">
                        <p class="mb-2"><strong>Name:</strong> {{ athlete['firstname'] }} {{ athlete['lastname'] }}</p>
                        <p class="mb-2"><strong>Username:</strong> {{ athlete['username'] }}</p>
                        <p class="mb-2"><strong>City:</strong> {{ athlete['city'] }}</p>
                        <p class="mb-2"><strong>State:</strong> {{ athlete['state'] }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</main>