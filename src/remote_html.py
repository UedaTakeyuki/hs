#-*- coding:utf-8 -*-
# Copy Right Takeyuki UEDA  © 2019 -
import textwrap

msg = textwrap.dedent('''\
<!--
 * @author Dr. Takeyuki UEDA
 * @copyright Copyright© Atelier UEDA 2019 - All rights reserved.
-->

<!-- https://stackoverflow.com/questions/12993835/passing-a-custom-python-function-into-a-tornado-template -->
{% import pprint %}
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="description" content="Base of Vuetify Example">
    <meta name="viewport" content="width=device-width">
    <title>Home Station remote</title>
    <link href='https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons' rel="stylesheet" type="text/css">
    <link href="https://unpkg.com/vuetify/dist/vuetify.min.css" rel="stylesheet" type="text/css"></link>
    <script src="https://unpkg.com/vue/dist/vue.js"></script>
    <script src="https://unpkg.com/vuetify/dist/vuetify.js"></script>
  </head>
  <body>
    <div id="app">
      <v-app>

        <h1>Home Station remote</h1>

        <v-text-field
         v-model="content_str"
         label="YouTube content id or url"
        >
        </v-text-field>
        <v-btn @click="submit();">{{id}}</v-btn>
        <p id="result"></p>

      </v-app>
    </div>

    <script>
      //-------------------------------------------------------------
      //
      // Vue
      //
      //-------------------------------------------------------------
      var vue = new Vue({
        el: '#app',
        data: {
          sock: "",
          content_str: ""
        },
        methods: {
          submit: function(){
//            this.sock.send("uyHbcHcJ9QQ");
//            this.sock.send(this.content_str);
            this.sock.send(this.videoId);
          },
        },
        computed: {
          videoId: function(){
            // http://q.hatena.ne.jp/1327668301
            res = /^([-\w]{11})$/.exec(this.content_str);
            if (res && res.length == 2){
              return res[1];
            } else {
              res = /[/?=]([-\w]{11})/.exec(this.content_str);
              if (res && res.length == 2){
                return res[1];
              } else {
                return "";
              }
            }
          },
        }
      })
    </script>
    <script>
      //-------------------------------------------------------------
      //
      // WS handler
      //
      //-------------------------------------------------------------
      vue.sock = ConnectWS({{id}}, document.getElementById("result"));

      function ConnectWS(id, element) {
        var url = "ws://" + location.hostname + ":8888/remote_connection/"+id;
        var sock = new WebSocket(url);
        // 接続
        sock.addEventListener('open',function(e){
          console.log('Socket 接続成功');
        });
        // When message 
        sock.addEventListener('message',function(e){
          console.log(e.data);
          element.innerHTML
            = e.data;
        });
        // When close 
        sock.addEventListener('close',function(e){
          console.log('Socket closed.');
          vue.sock = ConnectWS({{id}}, document.getElementById("result"));
        });
/*
        document.querySelector("button").addEventListener("click", function(){
          let date = new Date();
          sock.send("uyHbcHcJ9QQ");
        });
*/
        return sock;

      }
    </script>
  </body>
</html>
''')