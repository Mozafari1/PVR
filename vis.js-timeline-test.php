<?php
// DB Connection
$conn = mysqli_connect("localhost", "root", "", "visjs");
if (mysqli_connect_errno()) {
    echo "Connecting to DB failed: " . mysqli_connect_error();
}

// Select Query
$sql = 'SELECT * FROM vis';
$res = mysqli_query($conn, $sql);

// Create Array  and push your data 
$stack = array();
while ($datarows =mysqli_fetch_array( $res, MYSQLI_ASSOC )) {
  array_push($stack, $datarows);
 
}
// Encode your stack array
$Encoded_JSON_Array = json_encode( $stack );

?>


<!doctype html>
<html>
<head>
  <title>Timeline</title>
  <script type="text/javascript" src="https://unpkg.com/vis-timeline@latest/standalone/umd/vis-timeline-graph2d.min.js"></script>
  <link href="https://unpkg.com/vis-timeline@latest/styles/vis-timeline-graph2d.min.css" rel="stylesheet" type="text/css" />
  <style type="text/css">
    #visualization {
      width: 600px;
      height: 400px;
      border: 1px solid lightgray;
    }
  </style>
</head>
<body>
<div id="visualization"></div>

<script type="text/javascript">
  // DOM element where the Timeline will be attached
  var container = document.getElementById('visualization');
// Create a DataSet (allows two way data-binding)
  

// CREATE NEW ARRAY, THEN CARRY ON AND CONVERT THE PHP ARRAY TO A JAVASCRIPT ARRAY
const new_Array = []
var Encoded_JSON_Array = <?php echo $Encoded_JSON_Array ?> ; // CONVERTS TO JS ARRAY

// !IMPORTANT 
// PUSH DATA INTO YOUR NEW ARRAY AS OBJECTS. NOTES! vis.js DATASET MUST HAVE THIS {id: , content: , start: }. THEY ARE CONSTANTS THAT YOU CANT CHANGE IT. 
for (let i = 0; i <Encoded_JSON_Array.length; i++){
  new_Array.push({id: Number(Encoded_JSON_Array[i].id), content: Encoded_JSON_Array[i].content, start: Encoded_JSON_Array[i].start_date, end: Encoded_JSON_Array[i].end_date})
}

// CALL YOUR ARRAY IN DATASET, THEN YOU ARE GOOD TO GO!
var items = new vis.DataSet(new_Array);

  // Configuration for the Timeline
  var options = {};

  // Create a Timeline
  var timeline = new vis.Timeline(container, items, options);
</script>
</body>
</html>
