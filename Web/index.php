<!doctype html>
<html lang="en">

<head>

  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <link rel="apple-touch-icon" sizes="76x76" href="./assets/img/favicon.png">
  <link rel="icon" type="image/png" href="./assets/img/favicon.png">


  <title>NPCamp Availability of National Park Campsites</title>
  <meta content="アメリカ国立公園キャンプ場の空き情報まとめサイト。This site automatically totals the availability of national park campsites." name="description">
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
  <!--     Fonts and icons     -->
  <link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Roboto+Slab:400,700|Material+Icons" />
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/latest/css/font-awesome.min.css">
  <!-- Material Icons -->
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
  <!-- Material Kit CSS -->
  <link href="./assets/css/material-kit.css?v=3.0.0" rel="stylesheet" />
  <link href="./assets/css/index.css" rel="stylesheet" />


  <link rel="stylesheet" href="./Web/assets/css/index.css">
  <link href='//use.fontawesome.com/releases/v5.11.0/css/all.css' rel='stylesheet' type='text/css' />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome-animation/0.0.10/font-awesome-animation.css" type="text/css" media="all" />

  <!-- Global site tag (gtag.js) - Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-SVQTD22Y56"></script>
  <script>
    window.dataLayer = window.dataLayer || [];

    function gtag() {
      dataLayer.push(arguments);
    }
    gtag('js', new Date());

    gtag('config', 'G-SVQTD22Y56');
  </script>

</head>

<body class="index-page bg-gray-200">

  <!-- Navbar -->
  <?php include('templates/navbar.html') ?>

  <!-- Header -->
  <?php include('templates/header.html') ?>

  <!-- Main body -->
  <div class="card card-body blur shadow-blur mx-3 mx-md-4 mt-n6">

    <!-- Count -->
    <?php include('pages/count.html') ?>

    <!-- Campsite data -->
    <h2>West</h2>

    <?php include('pages/North_Cascades.html') ?>

    <?php include('pages/Olympic.html') ?>

    <?php include('pages/Mount_Rainier.html') ?>

    <?php include('pages/Lassen_Volcanic.html') ?>

    <?php include('pages/Yosemite.html') ?>

    <?php include('pages/Death_Valley.html') ?>

    <?php include('pages/Sequoia_and_Kings_Canyon.html') ?>

    <?php include('pages/Pinnacles.html') ?>

    <?php include('pages/Channel_Islands.html') ?>

    <?php include('pages/Joshua_Tree.html') ?>

    <?php include('pages/Great_Basin.html') ?>

    <?php include('pages/Yellowstone.html') ?>

    <?php include('pages/Grand_Teton.html') ?>

    <?php include('pages/Zion.html') ?>

    <?php include('pages/Bryce_Canyon.html') ?>

    <?php include('pages/Capitol_Reef.html') ?>

    <?php include('pages/Canyonlands.html') ?>

    <?php include('pages/Arches.html') ?>

    <?php include('pages/Grand_Canyon.html') ?>

    <?php include('pages/Rocky_Mountain') ?>
    

  </div>


  <!-- Footer -->
  <?php include('templates/footer.html') ?>
</body>



<!--   Core JS Files   -->
<script src="./assets/js/core/popper.min.js" type="text/javascript"></script>
<script src="./assets/js/core/bootstrap.min.js" type="text/javascript"></script>
<script src="./assets/js/plugins/perfect-scrollbar.min.js"></script>

<!--  Plugin for TypedJS, full documentation here: https://github.com/inorganik/CountUp.js -->
<script src="./assets/js/plugins/countup.min.js"></script>

<script src="./assets/js/plugins/choices.min.js"></script>
<script src="./assets/js/plugins/prism.min.js"></script>
<script src="./assets/js/plugins/highlight.min.js"></script>

<!--  Plugin for Parallax, full documentation here: https://github.com/dixonandmoe/rellax -->
<script src="./assets/js/plugins/rellax.min.js"></script>
<!--  Plugin for TiltJS, full documentation here: https://gijsroge.github.io/tilt.js/ -->
<script src="./assets/js/plugins/tilt.min.js"></script>
<!--  Plugin for Selectpicker - ChoicesJS, full documentation here: https://github.com/jshjohnson/Choices -->
<script src="./assets/js/plugins/choices.min.js"></script>

<!--  Plugin for Parallax, full documentation here: https://github.com/wagerfield/parallax  -->
<script src="./assets/js/plugins/parallax.min.js"></script>

<!-- Control Center for Material UI Kit: parallax effects, scripts for the example pages etc -->


<script src="./assets/js/material-kit.min.js?v=3.0.0" type="text/javascript"></script>

<script type="text/javascript">
  if (document.getElementById('state1')) {
    const countUp = new CountUp('state1', document.getElementById("state1").getAttribute("countTo"));
    if (!countUp.error) {
      countUp.start();
    } else {
      console.error(countUp.error);
    }
  }
  if (document.getElementById('state2')) {
    const countUp1 = new CountUp('state2', document.getElementById("state2").getAttribute("countTo"));
    if (!countUp1.error) {
      countUp1.start();
    } else {
      console.error(countUp1.error);
    }
  }
  if (document.getElementById('state3')) {
    const countUp2 = new CountUp('state3', document.getElementById("state3").getAttribute("countTo"));
    if (!countUp2.error) {
      countUp2.start();
    } else {
      console.error(countUp2.error);
    };
  }
</script>

</html>