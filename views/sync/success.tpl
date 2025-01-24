% rebase('layout.tpl', title='Sync Successful')
<main class="container mt-4">
    <div class="alert alert-success">
        <h4>Sync Successful!</h4>
        <p>Successfully synced {{activity_count}} activities.</p>
    </div>
    <a href="/heatmap" class="btn btn-primary">View Heatmap</a>
    <a href="/sync" class="btn btn-secondary">Sync More Activities</a>
</main> 