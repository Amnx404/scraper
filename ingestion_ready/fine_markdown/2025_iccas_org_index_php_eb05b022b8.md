# ICCAS 2025

The 25th International Conference on Control, Automation and Systems (ICCAS 2025)

URL: http://2025.iccas.org

This document outlines the REST API routes available for the ICCAS 2025 website.

## Root

*   `GET /`

## Batch Processing

*   `POST /batch/v1`

## oEmbed

*   `GET /oembed/1.0/`
*   `GET /oembed/1.0/embed`
*   `GET /oembed/1.0/proxy`

## Wordfence

*   `GET /wordfence/v1/`
*   `GET /wordfence/v1/authenticate`
*   `POST /wordfence/v1/authenticate`
*   `POST /wordfence/v1/authenticate-premium`
*   `GET /wordfence/v1/config`
*   `POST /wordfence/v1/config`
*   `PUT /wordfence/v1/config`
*   `PATCH /wordfence/v1/config`
*   `POST /wordfence/v1/disconnect`
*   `PUT /wordfence/v1/disconnect`
*   `PATCH /wordfence/v1/disconnect`
*   `POST /wordfence/v1/premium-connect`
*   `PUT /wordfence/v1/premium-connect`
*   `PATCH /wordfence/v1/premium-connect`
*   `GET /wordfence/v1/scan/issues`
*   `POST /wordfence/v1/scan`
*   `DELETE /wordfence/v1/scan`
*   `POST /wordfence/v1/scan/issue`
*   `PUT /wordfence/v1/scan/issue`
*   `PATCH /wordfence/v1/scan/issue`

## WP Super Cache

*   `GET /wp-super-cache/v1/`
*   `GET /wp-super-cache/v1/settings`
*   `POST /wp-super-cache/v1/settings`
*   `GET /wp-super-cache/v1/status`
*   `GET /wp-super-cache/v1/stats`
*   `GET /wp-super-cache/v1/cache`
*   `POST /wp-super-cache/v1/cache`
*   `POST /wp-super-cache/v1/preload`
*   `POST /wp-super-cache/v1/cache/test`
*   `GET /wp-super-cache/v1/plugins`
*   `POST /wp-super-cache/v1/plugins`

## GeneratePress

*   `GET /generatepress/v1/`
*   `POST /generatepress/v1/reset`
*   `PUT /generatepress/v1/reset`
*   `PATCH /generatepress/v1/reset`

## Elementor

*   `GET /elementor/v1/`
*   `GET /elementor/v1/globals`
*   `GET /elementor/v1/globals/colors`
*   `GET /elementor/v1/globals/colors/{id}`
*   `POST /elementor/v1/globals/colors/{id}`
*   `DELETE /elementor/v1/globals/colors/{id}`
*   `GET /elementor/v1/globals/typography`
*   `GET /elementor/v1/globals/typography/{id}`
*   `POST /elementor/v1/globals/typography/{id}`
*   `DELETE /elementor/v1/globals/typography/{id}`
*   `GET /elementor/v1/favorites`
*   `POST /elementor/v1/favorites/{id}`
*   `DELETE /elementor/v1/favorites/{id}`
*   `GET /elementor/v1/kit-elements-defaults`
*   `POST /elementor/v1/kit-elements-defaults/{type}`
*   `PUT /elementor/v1/kit-elements-defaults/{type}`
*   `PATCH /elementor/v1/kit-elements-defaults/{type}`
*   `DELETE /elementor/v1/kit-elements-defaults/{type}`
*   `GET /elementor/v1/site-navigation/recent-posts`
*   `POST /elementor/v1/site-navigation/add-new-post`
*   `GET /elementor/v1/checklist`
*   `GET /elementor/v1/checklist/{id}`
*   `GET /elementor/v1/checklist/steps`
*   `GET /elementor/v1/checklist/steps/{id}`
*   `POST /elementor/v1/checklist/steps/{id}`
*   `PUT /elementor/v1/checklist/steps/{id}`
*   `PATCH /elementor/v1/checklist/steps/{id}`
*   `GET /elementor/v1/checklist/user-progress`
*   `POST /elementor/v1/checklist/user-progress`
*   `PUT /elementor/v1/checklist/user-progress`
*   `PATCH /elementor/v1/checklist/user-progress`
*   `GET /elementor/v1/template-library/templates`
*   `POST /elementor/v1/template-library/templates`
*   `GET /elementor/v1/send-event`
*   `POST /elementor/v1/send-event`

## Two-Factor Authentication

*   `GET /two-factor/1.0/`
*   `DELETE /two-factor/1.0/totp`
*   `POST /two-factor/1.0/totp`
*   `POST /two-factor/1.0/generate-backup-codes`

## WordPress REST API (wp/v2)

### Posts

*   `GET /wp/v2/posts`
*   `POST /wp/v2/posts`
*   `GET /wp/v2/posts/{id}`
*   `POST /wp/v2/posts/{id}`
*   `PUT /wp/v2/posts/{id}`
*   `PATCH /wp/v2/posts/{id}`
*   `DELETE /wp/v2/posts/{id}`
*   `GET /wp/v2/posts/{id}/revisions`
*   `GET /wp/v2/posts/{id}/revisions/{id}`
*   `DELETE /wp/v2/posts/{id}/revisions/{id}`
*   `GET /wp/v2/posts/{id}/autosaves`
*   `POST /wp/v2/posts/{id}/autosaves`
*   `GET /wp/v2/posts/{id}/autosaves/{id}`

### Pages

*   `GET /wp/v2/pages`
*   `POST /wp/v2/pages`
*   `GET /wp/v2/pages/{id}`
*   `POST /wp/v2/pages/{id}`
*   `PUT /wp/v2/pages/{id}`
*   `PATCH /wp/v2/pages/{id}`
*   `DELETE /wp/v2/pages/{id}`
*   `GET /wp/v2/pages/{id}/revisions`
*   `GET /wp/v2/pages/{id}/revisions/{id}`
*   `DELETE /wp/v2/pages/{id}/revisions/{id}`
*   `GET /wp/v2/pages/{id}/autosaves`
*   `POST /wp/v2/pages/{id}/autosaves`
*   `GET /wp/v2/pages/{id}/autosaves/{id}`

### Media

*   `GET /wp/v2/media`
*   `POST /wp/v2/media`
*   `GET /wp/v2/media/{id}`
*   `POST /wp/v2/media/{id}`
*   `PUT /wp/v2/media/{id}`
*   `PATCH /wp/v2/media/{id}`
*   `DELETE /wp/v2/media/{id}`
*   `POST /wp/v2/media/{id}/post-process`
*   `POST /wp/v2/media/{id}/edit`

### Menu Items

*   `GET /wp/v2/menu-items`
*   `POST /wp/v2/menu-items`
*   `GET /wp/v2/menu-items/{id}`
*   `POST /wp/v2/menu-items/{id}`
*   `PUT /wp/v2/menu-items/{id}`
*   `PATCH /wp/v2/menu-items/{id}`
*   `DELETE /wp/v2/menu-items/{id}`
*   `GET /wp/v2/menu-items/{id}/autosaves`
*   `POST /wp/v2/menu-items/{id}/autosaves`
*   `GET /wp/v2/menu-items/{id}/autosaves/{id}`

### Blocks

*   `GET /wp/v2/blocks`
*   `POST /wp/v2/blocks`
*   `GET /wp/v2/blocks/{id}`
*   `POST /wp/v2/blocks/{id}`
*   `PUT /wp/v2/blocks/{id}`
*   `PATCH /wp/v2/blocks/{id}`
*   `DELETE /wp/v2/blocks/{id}`
*   `GET /wp/v2/blocks/{id}/revisions`
*   `GET /wp/v2/blocks/{id}/revisions/{id}`
*   `DELETE /wp/v2/blocks/{id}/revisions/{id}`
*   `GET /wp/v2/blocks/{id}/autosaves`
*   `POST /wp/v2/blocks/{id}/autosaves`
*   `GET /wp/v2/blocks/{id}/autosaves/{id}`

### Templates

*   `GET /wp/v2/templates/{slug}`
*   `POST /wp/v2/templates/{slug}`
*   `PUT /wp/v2/templates/{slug}`
*   `PATCH /wp/v2/templates/{slug}`
*   `DELETE /wp/v2/templates/{slug}`
*   `GET /wp/v2/templates/{slug}/revisions`
*   `GET /wp/v2/templates/{slug}/revisions/{id}`
*   `DELETE /wp/v2/templates/{slug}/revisions/{id}`
*   `GET /wp/v2/templates/{slug}/autosaves`
*   `POST /wp/v2/templates/{slug}/autosaves`
*   `GET /wp/v2/templates/{slug}/autosaves/{id}`
*   `GET /wp/v2/templates`
*   `POST /wp/v2/templates`
*   `GET /wp/v2/templates/lookup`

### Template Parts

*   `GET /wp/v2/template-parts/{slug}`
*   `POST /wp/v2/template-parts/{slug}`
*   `PUT /wp/v2/template-parts/{slug}`
*   `PATCH /wp/v2/template-parts/{slug}`
*   `DELETE /wp/v2/template-parts/{slug}`
*   `GET /wp/v2/template-parts/{slug}/revisions`
*   `GET /wp/v2/template-parts/{slug}/revisions/{id}`
*   `DELETE /wp/v2/template-parts/{slug}/revisions/{id}`
*   `GET /wp/v2/template-parts/{slug}/autosaves`
*   `POST /wp/v2/template-parts/{slug}/autosaves`
*   `GET /wp/v2/template-parts/{slug}/autosaves/{id}`
*   `GET /wp/v2/template-parts`
*   `POST /wp/v2/template-parts`
*   `GET /wp/v2/template-parts/lookup`

## WordPress Site Health

*   `GET /wp-site-health/v1/`

## WordPress Block Editor

*   `GET /wp-block-editor/v1/`

## WordPress Abilities

*   `GET /wp-abilities/v1/`
