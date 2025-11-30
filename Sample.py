def plotly_line(df, title="", x_label=None, y_label=None, show_range=True, markers=False):
    """
    Robust plot helper: resets index for time/numeric x, coerces y-columns to numeric,
    drops rows without numeric data, and then calls px.line.
    """
    if df is None or getattr(df, "empty", True):
        st.info("No data available for this chart.")
        return

    df_plot = df.copy()

    # If first column is the index (datetime or numeric), reset it
    try:
        if isinstance(df_plot.index, pd.DatetimeIndex) or pd.api.types.is_numeric_dtype(df_plot.index):
            df_plot = df_plot.reset_index()
            # rename index column to 'x' friendly name if unnamed
            if df_plot.columns[0] == 0 or df_plot.columns[0] == "":
                df_plot = df_plot.rename(columns={df_plot.columns[0]: "x"})
    except Exception:
        # fallback: attempt reset_index anyway
        try:
            df_plot = df_plot.reset_index()
        except Exception:
            pass

    # If only a single column (no explicit x), ensure column names are clean
    if df_plot.shape[1] == 1:
        df_plot.columns = ["value"]

    # Identify x and y columns
    x_col = df_plot.columns[0]
    y_cols = list(df_plot.columns[1:]) if df_plot.shape[1] > 1 else [df_plot.columns[0]]

    # Coerce y columns to numeric (safe)
    for c in y_cols:
        df_plot[c] = pd.to_numeric(df_plot[c], errors="coerce")

    # If x column accidentally numeric-like string, try to convert to datetime if possible
    if pd.api.types.is_object_dtype(df_plot[x_col]):
        try:
            df_plot[x_col] = pd.to_datetime(df_plot[x_col], errors="ignore")
        except Exception:
            pass

    # Drop rows where all y columns are NaN
    if len(y_cols) > 1:
        df_plot = df_plot.dropna(subset=y_cols, how="all")
    else:
        df_plot = df_plot.dropna(subset=[y_cols[0]])

    # If nothing left to plot, inform user
    if df_plot.shape[0] == 0 or (len(y_cols) > 0 and df_plot[y_cols].dropna(how="all").shape[0] == 0):
        st.info("No numeric data available to plot after cleaning.")
        return

    # Optional: cast index column to str/datetime depending on type so px behaves
    try:
        fig = px.line(df_plot, x=x_col if len(y_cols) > 0 else None, y=y_cols if len(y_cols) > 1 else y_cols[0],
                      title=title, markers=markers)
        if x_label or y_label:
            fig.update_layout(xaxis_title=x_label or "", yaxis_title=y_label or "")
        if show_range:
            fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)))
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        # Show debugging info to help if it still fails
        st.error("Plotly failed to build the figure. Showing data types and a sample of the cleaned dataframe:")
        st.write("dtypes:", df_plot.dtypes.to_dict())
        st.write(df_plot.head(10))
        st.exception(e)
        return
