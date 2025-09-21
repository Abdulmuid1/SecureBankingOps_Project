{{- define "accounts.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- define "accounts.fullname" -}}
{{ include "accounts.name" . }}-{{ .Release.Name }}
{{- end }}

{{- define "accounts.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end }}
