{{- define "auth-service.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "auth-service.fullname" -}}
{{ include "auth-service.name" . }}-{{ .Release.Name }}
{{- end }}

{{- define "auth-service.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}
