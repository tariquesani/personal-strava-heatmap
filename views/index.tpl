% rebase('layout.tpl', title='Home Page')
<main class="container mt-4 pt-3">
    <div class="row justify-content-center">
        <div class="col-md-10">
            <div class="row">
                % if athlete:
                <div class="col-md-4">
                    <div class="card mb-4">
                        <div class="card-body text-center">
                            <h3 class="card-title">Athlete Profile</h3>
                            <img src="{{ athlete['profile'] }}" alt="Profile Image" class="img-fluid rounded-circle mb-3">
                            <p class="mb-2"><strong>Name:</strong> {{ athlete['firstname'] }} {{ athlete['lastname'] }}</p>
                            <p class="mb-2"><strong>Username:</strong> {{ athlete['username'] }}</p>
                            <p class="mb-2"><strong>City:</strong> {{ athlete['city'] }}</p>
                            <p class="mb-2"><strong>State:</strong> {{ athlete['state'] }}</p>
                        </div>
                    </div>
                </div>
                % end
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body">
                            <h2 class="card-title text-center">System Checklist</h2>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item">.env file: <span class="{{'text-success' if checklist['env_file'] else 'text-danger'}}">{{'Present' if checklist['env_file'] else 'Missing'}}</span></li>
                                <li class="list-group-item">Strava credentials: <span class="{{'text-success' if checklist['strava_credentials'] else 'text-danger'}}">{{'Valid' if checklist['strava_credentials'] else 'Invalid'}}</span></li>
                                <li class="list-group-item">Data files:
                                    <ul class="list-group">
                                        <li class="list-group-item">strava_activities.json: <span class="{{'text-success' if checklist['data_files']['strava_activities'] else 'text-danger'}}">{{'Present' if checklist['data_files']['strava_activities'] else 'Missing'}}</span></li>
                                        <li class="list-group-item">strava_athlete.json: <span class="{{'text-success' if checklist['data_files']['strava_athlete'] else 'text-danger'}}">{{'Present' if checklist['data_files']['strava_athlete'] else 'Missing'}}</span></li>
                                    </ul>
                                </li>
                            </ul>
                            <div class="text-center mt-3">
                                <a href="/heatmap" class="btn btn-primary">View Heatmap</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</main>