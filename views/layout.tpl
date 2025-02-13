<!DOCTYPE html>
<html class="h-100">
<head>
    <title>{{get('title', ' ')}} - {{athlete.get('firstname', 'Athlete')}}'s Running Heatmap</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <link rel="stylesheet" type="text/css" href="/static/style.css">
    <link rel="icon" type="image/icon" href="/static/favicon.ico">
</head>
<body class="d-flex flex-column h-100">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark py-0">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link py-2 my-0" href="/"><i class="bi bi-house"></i> </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link py-2 my-0" href="/heatmap/routes"><i class="bi bi-repeat"></i> Routes</a>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle py-2 my-0" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="bi bi-map"></i> Heatmap
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="/heatmap">Static</a></li>
                            <li><a class="dropdown-item" href="/heatmap/time">Timelapse</a></li>
                            <li><a class="dropdown-item" href="/heatmap/single">One at a time</a></li>
                        </ul>
                    </li>                    
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle py-2 my-0" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="bi bi-arrow-repeat"></i> Sync
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="/sync">Full Sync</a></li>
                            <li><a class="dropdown-item" href="/sync/inc">Incremental Sync</a></li>
                            <li><a class="dropdown-item" href="/sync/athlete">Athlete Sync</a></li>
                        </ul>
                    </li>                    
                </ul>
                <a class="navbar-brand py-2 my-0" href="/">
                    <img src="{{athlete.get('profile', 'static/blank-profile-picture.png')}}" class="rounded-circle" width="25" height="25">
                    {{athlete.get('firstname', 'Athlete')}}'s Running Heatmap
                </a>
            </div>
        </div>
    </nav>
    
    <main class="flex-shrink-0 flex-grow-1">
        {{!base}}
    </main>
    
    <footer class="footer mt-auto py-3 bg-light">
        <div class="container text-center">
            <p class="text-muted mb-0">&copy; 2025 Personal Strava Heatmap Project</p>
        </div>
    </footer>

    <!-- Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
