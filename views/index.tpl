% rebase('layout.tpl', title='Home Page')
<main class="container mt-4 pt-3 d-flex justify-content-center">
    <div class="col-md-6">
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
</main>