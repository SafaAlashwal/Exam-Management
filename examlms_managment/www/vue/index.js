const App = Vue.createApp({
    data() {
      return {
        name_person: 'ahmed',
        age: 50,
        questions: {},
      };
    },
    delimiters: ['[[', ']]'],
    methods: {
      getOptions(question) {
        const options = [];
        for (let i = 1; i <= 4; i++) {
          const optionKey = `option_${i}`;
          if (question[optionKey] !== null && question[optionKey] !== undefined) {
            options.push(question[optionKey]);
          }
        }
        console.log(options);
        return options;
      },
    },
    
    computed: {
        async get_prop() {
          let res = await $.ajax({
            url: '/api/method/examlms_managment.www.vue.index.get_prop',
            type: 'GET',
          });
          console.log(res.message);
          this.questions = res.message;
        },

      //   send_answer() {
      //     const csrfToken = frappe.csrf_token;
  
      //     $.ajax({
      //       type: 'POST',
      //       url: '/api/method/exams_managment.www.vue.index.send_answer',
      //       dataType: 'json',
      //       headers: {
      //         'X-Frappe-CSRF-Token': csrfToken,
      //       },
      //       success: function (response) {
      //         console.log(response.message);
      //       },
      //       error: function (xhr, status, error) {
      //         console.error(xhr.responseText);
      //       },
      //     });
      //   },
  
      //   createNewDoc() {
      //     $.ajax({
      //       method: "POST",
      //       url: "/api/method/your_app.your_module.create_new_doc",
      //       success: function(response) {
      //         console.log("Created new document with name: " + response);
      //       },
      //       error: function(xhr, status, error) {
      //         console.error(xhr.responseText);
      //       }
      //     });
  
    //   async send_doc() {
    //     const docData = {
    //       question: 'hhhhhhhhhh',
    //       option_1: 'h',
    //       option_2: 'y',
    //       option_3: 'z',
    //     };
  
    //     try {
    //       const response = await fetch(
    //         '/api/method/exams_managment.www.vue.index.send_doc',
    //         {
    //           method: 'POST',
    //           headers: {
    //             'Content-Type': 'application/json',
    //           },
    //           body: JSON.stringify(docData),
    //         }
    //       );
  
    //       const data = await response.json();
    //       console.log(data.message);
    //     } catch (error) {
    //       console.error('ط­ط¯ط« ط®ط·ط£ ط£ط«ظ†ط§ط، ط¥ط±ط³ط§ظ„ ط§ظ„ط¨ظٹط§ظ†ط§طھ ط¥ظ„ظ‰ ط¯ظˆظƒطھط§ظٹط¨:', error);
    //     }
    //   },
    },

  });
  
  App.mount('#app');
  