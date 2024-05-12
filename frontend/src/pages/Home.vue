<template>
  <div class="max-w-3xl py-12 mx-auto">


    <ul>{{ action }}</ul>

  </div>
</template>

<script>
import { Dialog , createListResource} from 'frappe-ui'

const action = createListResource({
  doctype: 'Question',
  // fields:["question"],
  limit: 10,
})


cd
</script>
