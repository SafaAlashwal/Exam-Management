<template>
  <div class="space-y-4">
    <div
      class="flex items-center justify-between"
      v-for="item in departmentsObj.data"
      :key="item.department"
    >
      <div>
        {{ item.department }}
      </div>
      <Badge>{{ item }}</Badge>
    </div>
  </div>
  <Button @click="departmentsObj.next()"> Next Page </Button>
</template>
<script setup>
import { createListResource } from 'frappe-ui'
let departmentsObj = createListResource({
  doctype: 'Department',
  fields: ['department'],
  orderBy: 'department desc',
  start: 0,
  pageLength: 5,
})
departmentsObj.fetch()
</script>