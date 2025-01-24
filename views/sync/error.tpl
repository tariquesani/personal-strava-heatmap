% rebase('layout.tpl', title='Sync Error')
<main class="container mt-4">
    <div class="alert alert-danger">
        <h4>Error During Sync</h4>
        <p>{{error}}</p>
    </div>
    <a href="/sync" class="btn btn-primary">Try Again</a>
</main> 