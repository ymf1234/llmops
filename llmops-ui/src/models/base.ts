// 基础响应数据格式
export type BaseResponse<T> = {
  code: number
  message: string
  data: T
}

// 数据分页响应数据格式
export type BasePaginatorResponse<T> = {
  list: Array<T>
  paginator: {
    total_page: number
    total_record: number
    current_page: number
    page_size: number
  }
}
