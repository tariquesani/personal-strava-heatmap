% rebase('layout.tpl', title='Athlete')

<h1>Athlete fetched from Strava</h1>

<p>Name: {{ athlete['firstname'] }} {{ athlete['lastname'] }}</p>
<p>Username: {{ athlete['username'] }}</p>
<p>City: {{ athlete['city'] }}</p>