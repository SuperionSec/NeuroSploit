export interface PaginationParams {
  current?: number;
  pageSize?: number;
  [key: string]: any;
}

export interface ProTableRequestParams extends PaginationParams {
  [key: string]: any;
}

export interface ProTableResponse<T> {
  data: T[];
  success: boolean;
  total: number;
}

export interface BackendListResponse<T> {
  data?: T[];
  total?: number;
  page?: number;
  per_page?: number;
  scans?: T[];
  reports?: T[];
  users?: T[];
  [key: string]: T[] | number | undefined;
}

export function convertPaginationToBackend(params: PaginationParams): Record<string, string | number> {
  const converted: Record<string, string | number> = {};

  if (params.current) {
    converted.page = params.current;
  }
  if (params.pageSize) {
    converted.per_page = params.pageSize;
  }

  Object.keys(params).forEach((key) => {
    if (key !== 'current' && key !== 'pageSize') {
      converted[key] = params[key] as string | number;
    }
  });

  return converted;
}

export function convertBackendToProTable<T>(response: BackendListResponse<T>): ProTableResponse<T> {
  let data: T[] = [];
  let total = 0;

  if (Array.isArray(response.data)) {
    data = response.data;
    total = response.total ?? data.length;
  } else if (Array.isArray(response.scans)) {
    data = response.scans;
    total = response.total ?? data.length;
  } else if (Array.isArray(response.reports)) {
    data = response.reports;
    total = response.total ?? data.length;
  } else if (Array.isArray(response.users)) {
    data = response.users;
    total = response.total ?? data.length;
  }

  return {
    data,
    success: true,
    total,
  };
}

export function createRequestInterceptor(getToken: () => string | null) {
  return (url: string, options: any) => {
    const token = getToken();
    if (token) {
      return {
        url,
        options: {
          ...options,
          headers: {
            ...options?.headers,
            Authorization: `Bearer ${token}`,
          },
        },
      };
    }
    return { url, options };
  };
}
