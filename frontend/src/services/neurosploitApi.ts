import {
  dashboardApi,
  scansApi,
  agentApi,
  reportsApi,
  vulnerabilitiesApi,
  vulnLabApi,
  schedulerApi,
} from './api'

export const neurosploitApi = {
  dashboard: {
    stats: dashboardApi.getStats,
    activityFeed: dashboardApi.getActivityFeed,
    recentScans: dashboardApi.getRecent,
    recentFindings: dashboardApi.getFindings,
    agentTasks: dashboardApi.getAgentTasks,
  },
  scans: {
    list: scansApi.list,
    get: scansApi.get,
    create: scansApi.create,
    start: scansApi.start,
    stop: scansApi.stop,
    pause: scansApi.pause,
    resume: scansApi.resume,
    delete: scansApi.delete,
    getEndpoints: scansApi.getEndpoints,
    getVulnerabilities: scansApi.getVulnerabilities,
  },
  autoPentest: {
    run: agentApi.autoPentest,
    getStatus: agentApi.getStatus,
    getLogs: agentApi.getLogs,
    getFindings: agentApi.getFindings,
    stop: agentApi.stop,
    pause: agentApi.pause,
    resume: agentApi.resume,
  },
  vulnerabilities: {
    list: vulnerabilitiesApi.getTypes,
    get: vulnerabilitiesApi.get,
    validate: vulnerabilitiesApi.validate,
  },
  reports: {
    list: reportsApi.list,
    generate: reportsApi.generate,
    downloadUrl: reportsApi.getDownloadUrl,
    viewUrl: reportsApi.getViewUrl,
    downloadZipUrl: reportsApi.getDownloadZipUrl,
    delete: reportsApi.delete,
  },
  vulnLab: {
    getTypes: vulnLabApi.getTypes,
    run: vulnLabApi.run,
    listChallenges: vulnLabApi.listChallenges,
    getChallenge: vulnLabApi.getChallenge,
    getStats: vulnLabApi.getStats,
    stopChallenge: vulnLabApi.stopChallenge,
    deleteChallenge: vulnLabApi.deleteChallenge,
  },
  scheduler: {
    list: schedulerApi.list,
    create: schedulerApi.create,
    delete: schedulerApi.delete,
    pause: schedulerApi.pause,
    resume: schedulerApi.resume,
    getAgentRoles: schedulerApi.getAgentRoles,
  },
}

export default neurosploitApi