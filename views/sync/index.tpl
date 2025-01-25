% rebase('layout.tpl', title='Sync Strava Activities')
<main class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-4">
            <h2 class="text-center mb-4">Sync Strava Activities</h2>
            
            % if start_date and end_date:
            <div class="alert alert-info mb-4">
                <p class="mb-0">
                    <strong>Existing activities:</strong><br>
                    From: {{start_date}} to {{end_date}}
                </p>
            </div>
            % end
            
            <form action="/sync/" method="POST" class="p-4 border rounded shadow-sm bg-white">
                <div class="mb-3">
                    <label for="start_date" class="form-label">Start Date:</label>
                    <input type="date" class="form-control" id="start_date" name="start_date" 
                           required placeholder="01-Jan-2025"
                           value="{{start_date if start_date else ''}}">
                </div>
                
                <div class="mb-3">
                    <label for="end_date" class="form-label">End Date (optional):</label>
                    <input type="date" class="form-control" id="end_date" name="end_date">
                    <div class="form-text">Leave blank to use today's date</div>
                </div>
                
                <div class="d-grid gap-2">
                    <button type="submit" class="btn btn-primary">Sync Activities</button>
                </div>
            </form>
        </div>
    </div>
</main> 