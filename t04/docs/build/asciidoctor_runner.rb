require 'asciidoctor'
require 'asciidoctor-diagram'
Asciidoctor.convert_file '/Users/wjq/Documents/deal-ii-fluid/gpt_CodeAnalysis-01/t04/docs/build/intermediate/addshell.adoc', to_file: '/Users/wjq/Documents/deal-ii-fluid/gpt_CodeAnalysis-01/t04/docs/build/output/addshell.html', safe: :unsafe, backend: 'html5', mkdirs: true, basedir: '/Users/wjq/Documents/deal-ii-fluid/gpt_CodeAnalysis-01/t04/docs/build/intermediate', attributes: 'imagesdir@=''images'' stylesheet@=''asciidoxy-no-toc.css'''
logger = Asciidoctor::LoggerManager.logger
exit 1 if (logger.respond_to? :max_severity) &&
  logger.max_severity &&
  logger.max_severity >= (::Logger::Severity.const_get 'FATAL')
