// 1.接口超时 100s
// 2.不需要写 api 前缀
// 3.我们经常使用 get 和 post, 需要对这两个发放进行封装
// 4.每次获取数据都要使用 response.json() 才可以获取数据,需要封装

import { apiPrefix, httpCode } from '@/config'
import { Message } from '@arco-design/web-vue'

// 1. 超时时间为 100s
const TIME_OUT = 100000
console.log('apiPrefix', apiPrefix)

// 创建基础配置
const baseFetchOptions = {
  method: 'GET',
  model: 'cors',
  credentials: 'include',
  headers: new Headers({
    'Content-Type': 'application/json',
  }),
  redirect: 'follow',
}

// 定义参数值的联合类型
type ParamValue = string | number | boolean | null | undefined

// fetch参数类型
type FetchOptionsType = Omit<RequestInit, 'body'> & {
  params?: Record<string, ParamValue>
  body?: BodyInit | Record<string, unknown> | null
}

// 2. 封装基础的 fetch 请求
export const baseFetch = <T>(url: string, fetchOptions: FetchOptionsType): Promise<T> => {
  // 将所有的配置信息合并起来
  const options: typeof baseFetchOptions & FetchOptionsType = Object.assign(
    {},
    baseFetchOptions,
    fetchOptions,
  )

  // 组装 url
  let urlWithPrefix = `${apiPrefix}${url.startsWith('/') ? url : `/${url}`}`

  // 结构出对应的请求方法, params, body参数
  const { method, params, body } = options

  // 如果是 GET 方法, 并传递了 params 参数
  if (method === 'GET' && params) {
    const paramsArray: string[] = []
    Object.keys(params).forEach((key: string) => {
      const value = params[key]
      if (value !== null && value !== undefined) {
        paramsArray.push(`${key}=${encodeURIComponent(String(value))}`)
      }
    })

    if (urlWithPrefix.search(/\?/) === -1) {
      urlWithPrefix += `?${paramsArray.join('&')}`
    } else {
      urlWithPrefix += `&${paramsArray.join('&')}`
    }

    delete options.params
  }

  if (body) {
    options.body = JSON.stringify(body)
  }

  return Promise.race([
    // 使用定时器来检测是否超时
    new Promise<never>((_, reject) => {
      setTimeout(() => {
        reject(new Error('请求超时'))
      }, TIME_OUT)
    }),

    // 发起请求
    new Promise<T>((resolve, reject) => {
      globalThis
        .fetch(urlWithPrefix, options as RequestInit)
        .then(async (res) => {
          console.log(res)
          if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`)
          }
          const json = await res.json()
          console.log(json)
          if (json.code === httpCode.success) {
            resolve(json)
          } else {
            Message.error(json.message)
            reject(new Error(json.message))
          }

          return res.json()
        })
        .then((data) => {
          resolve(data)
        })
        .catch((err: unknown) => {
          reject(err instanceof Error ? err : new Error(String(err)))
        })
    }),
  ]) as Promise<T>
}

export const request = <T = unknown>(url: string, option = {}): Promise<T> => {
  return baseFetch<T>(url, option)
}

// 3. 封装常用的 GET 和 POST 方法
export const get = <T = unknown>(url: string, options = {}): Promise<T> => {
  return request<T>(url, Object.assign({}, options, { method: 'GET' }))
}

export const post = <T = unknown>(
  url: string,
  body?: Record<string, unknown> | BodyInit,
  params?: Record<string, ParamValue>,
): Promise<T> => {
  return baseFetch<T>(url, {
    method: 'POST',
    body,
    params,
  })
}

export const put = <T = unknown>(
  url: string,
  body?: Record<string, unknown> | BodyInit,
  params?: Record<string, ParamValue>,
): Promise<T> => {
  return baseFetch<T>(url, {
    method: 'PUT',
    body,
    params,
  })
}

export const del = <T = unknown>(url: string, params?: Record<string, ParamValue>): Promise<T> => {
  return baseFetch<T>(url, {
    method: 'DELETE',
    params,
  })
}
