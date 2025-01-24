<!DOCTYPE html>
<html>
<head>
    <title>{{get('title', ' ')}} - Tarique's Running Heatmap</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="/static/style.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark py-0">
        <div class="container-fluid">
            <a class="navbar-brand py-2 my-0" href="/">Tarique's Running Heatmap</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link py-2 my-0" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link py-2 my-0" href="/heatmap">Heatmap</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link py-2 my-0" href="/sync">Sync</a>
                    </li>                    
                </ul>
            </div>
        </div>
    </nav>
    
    {{!base}}
    
    <footer class="footer mt-auto py-3 bg-light">
        <div class="container text-center">
            <p class="text-muted mb-0">&copy; 2025 Strava Heatmap Project</p>
        </div>
    </footer>

    <!-- Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
