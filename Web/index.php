<!doctype html>
<html lang="en">

<head>

  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <link rel="apple-touch-icon" sizes="76x76" href="./assets/img/favicon.png">
  <link rel="icon" type="image/png" href="./assets/img/favicon.png">


  <title>NPCamp Enjoy your camping</title>
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
    <section class="pt-3 pb-4" id="count-stats">
      <div class="container">
        <div class="row">
          <div class="col-lg-9 mx-auto py-3">
            <div class="row">
              <div class="col-md-4 position-relative">
                <div class="p-3 text-center">
                  <h1 class="text-gradient text-info"><span id="state1" countTo="4">0</span></h1>
                  <h5 class="mt-3">National Parks</h5>
                </div>
                <hr class="vertical dark">
              </div>
              <div class="col-md-4 position-relative">
                <div class="p-3 text-center">
                  <h1 class="text-gradient text-info"> <span id="state2" countTo="8">0</span>+</h1>
                  <h5 class="mt-3">Campgrounds</h5>
                </div>
                <hr class="vertical dark">
              </div>
              <div class="col-md-4">
                <div class="p-3 text-center">
                  <h1 class="text-gradient text-info"><span id="state3" countTo="2">0</span>+</h1>
                  <h5 class="mt-3">Weeks</h5>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Campsite data -->
    <h2>West</h2>
    <?php include('pages/Yosemite.html') ?>

    <?php include('pages/Grand_Canyon.html') ?>

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